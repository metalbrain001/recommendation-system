"""
This Module contains the test
cases for the movie api
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Movie
from movie.serializer import (
    MovieSerializer,
    MovieDetailSerializer,
)

MOVIES_URL = reverse("movie:movie-list")


def detail_url(movie_id):
    """
    Return movie detail URL.
    """

    return reverse("movie:movie-detail", args=[movie_id])


def create_movie(user, **params):
    """
    Helper function to create a new movie.
    """

    defaults = {
        "movie_id": 1,
        "title": "Toy Story",
        "genres": "Animation|Children's|Comedy",
    }
    defaults.update(params)
    movie = Movie.objects.create(user=user, **defaults)
    return movie


class publicMovieApiTests(TestCase):
    """
    Test the publicly available movies API.
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that authentication is
        required for retrieving movies.
        """

        res = self.client.get(MOVIES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class privateMovieApiTests(TestCase):
    """
    Test the private movies API.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@example.com",
            "testpass123",
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_movies(self):
        """
        Test retrieving movies.
        """

        create_movie(
            movie_id=1,
            title="Toy Story",
            genres="Animation|Children's|Comedy",
            user=self.user,
        )

        create_movie(
            movie_id=2,
            title="Jumanji",
            genres="Action|Adventure|Comedy",
            user=self.user,
        )

        res = self.client.get(MOVIES_URL)
        movies = Movie.objects.all().order_by("-movie_id")
        serializer = MovieSerializer(movies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_movie_limited_to_user(self):
        """
        Test list of movies returned are for
        the authenticated user.
        """

        user2 = get_user_model().objects.create_user(
            "user@example.com",
            "testpass123",
        )

        create_movie(
            movie_id=1,
            title="Toy Story",
            genres="Animation|Children's|Comedy",
            user=user2,
        )

        movie = create_movie(
            movie_id=2,
            title="Jumanji",
            genres="Action|Adventure|Comedy",
            user=self.user,
        )

        res = self.client.get(MOVIES_URL)
        movie = Movie.objects.filter(user=self.user)
        serializer = MovieSerializer(movie, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_create_movie_invalid(self):
        """
        Test creating a new movie with invalid payload.
        """

        payload = {
            "movie_id": "",
            "title": "",
            "genres": "",
        }

        res = self.client.post(MOVIES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_movie_detail(self):
        """
        Test viewing a movie detail.
        """

        movie = create_movie(user=self.user)
        url = detail_url(movie.movie_id)
        res = self.client.get(url)
        serializer = MovieDetailSerializer(movie)
        self.assertEqual(res.data, serializer.data)

    def test_create_movie_successful(self):
        """
        Test creating a new movie.
        """

        payload = {
            "movie_id": 22,
            "title": "Love Dont Cost",
            "genres": "Comedy|Drama|Romance",
        }

        res = self.client.post(MOVIES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        movie = Movie.objects.get(movie_id=res.data["movie_id"])
        for k, v in payload.items():
            self.assertEqual(v, getattr(movie, k))
        self.assertEqual(movie.user, self.user)

    def test_partial_update_movie(self):
        """
        Test updating a movie with PATCH.
        """

        movie = create_movie(user=self.user, title="Old Title")
        payload = {"title": "New Title"}
        url = detail_url(movie.movie_id)
        res = self.client.patch(url, payload)
        movie.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(movie.title, payload["title"])

    def test_full_update_movie(self):
        """
        Test updating a movie with PUT.
        """

        movie = create_movie(user=self.user, title="Old Title")
        payload = {
            "movie_id": movie.movie_id,
            "title": "Updated Title",
            "genres": "Updated Genre",
        }
        url = detail_url(movie.movie_id)
        res = self.client.put(url, payload)
        movie.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(movie.title, payload["title"])
        self.assertEqual(movie.genres, payload["genres"])

    def test_delete_movie(self):
        """
        Test deleting a movie.
        """

        movie = create_movie(user=self.user)
        url = detail_url(movie.movie_id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Movie.objects.filter(movie_id=movie.movie_id).exists())

    def test_unauthorized_movie_update(self):
        """
        Test that a movie cannot
        be updated by another user.
        """

        new_user = get_user_model().objects.create_user(
            email="newuser@example.com", password="newpass123"
        )
        movie = create_movie(user=new_user, title="Original Title")
        payload = {"title": "Hacked Title"}
        url = detail_url(movie.movie_id)
        res = self.client.patch(url, payload)
        movie.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(movie.title, "Original Title")

    def test_unauthorized_movie_delete(self):
        """
        Test that a movie cannot be deleted by another user.
        """

        new_user = get_user_model().objects.create_user(
            email="newuser@example.com", password="newpass123"
        )
        movie = create_movie(user=new_user)
        url = detail_url(movie.movie_id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Movie.objects.filter(movie_id=movie.movie_id).exists())

    def test_filter_movies_by_genre(self):
        """
        Test filtering movies by genre.
        """
        create_movie(
            movie_id=1, user=self.user, title="Toy Story", genres="Animation|Comedy"
        )
        create_movie(
            movie_id=2, user=self.user, title="Jumanji", genres="Action|Adventure"
        )

        res = self.client.get(MOVIES_URL, {"genres": "Animation"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 2)
        self.assertEqual(res.data["results"][0]["title"], "Jumanji")
        self.assertEqual(res.data["results"][0]["genres"], "Action|Adventure")
        self.assertEqual(res.data["results"][1]["title"], "Toy Story")
        self.assertEqual(res.data["results"][1]["genres"], "Animation|Comedy")

    def test_movie_list_pagination(self):
        """
        Test pagination of movie list.
        """

        for i in range(15):
            create_movie(user=self.user, movie_id=i + 1, title=f"Movie {i+1}")
        res = self.client.get(MOVIES_URL, {"page": 1})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue("next" in res.data or "previous" in res.data)
        self.assertTrue(len(res.data["results"]) <= 10)
