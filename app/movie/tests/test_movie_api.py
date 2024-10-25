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
