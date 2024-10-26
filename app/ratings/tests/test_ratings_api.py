"""
This module tests the ratings API.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ratings, Movie


RATINGS_URL = reverse("ratings:ratings-list")


def detail_url(rating_id):
    """
    Return rating detail URL.
    """
    return reverse("ratings:ratings-detail", args=[rating_id])


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
    ratings = Movie.objects.create(user=user, **defaults)
    return ratings


def create_rating(user, movie, rating_value=5):
    """
    Helper function to create a rating for a movie.
    """
    return Ratings.objects.create(user=user, movie=movie, rating=rating_value)


class PublicRatingApiTests(TestCase):
    """
    Test the public ratings API.
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that authentication is
        required for retrieving ratings.
        """

        res = self.client.get(RATINGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRatingApiTests(TestCase):
    """
    Test the private ratings API.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="other3@example.com", password="testpass123"
        )
        self.client.force_authenticate(self.user)
        self.movie = create_movie(user=self.user)

    def test_list_ratings(self):
        """
        Test retrieving a list of ratings.
        """

        movie1 = create_movie(user=self.user, movie_id=101, title="Toy Story")
        movie2 = create_movie(user=self.user, movie_id=202, title="Jumanji")

        # Create unique ratings for different movies
        create_rating(user=self.user, movie=movie1, rating_value=5)
        create_rating(user=self.user, movie=movie2, rating_value=4)
        res = self.client.get(RATINGS_URL)
        ratings = Ratings.objects.filter(user=self.user)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), ratings.count())

    def test_retrieve_rating_detail(self):
        """
        Test viewing a rating detail.
        """

        rating = create_rating(user=self.user, movie=self.movie, rating_value=4)
        url = detail_url(rating.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(float(res.data["rating"]), rating.rating)
        self.assertEqual(res.data["movie"], self.movie.movie_id)

    def test_create_rating(self):
        """
        Test creating a rating for a movie.
        """

        payload = {"movie": self.movie.movie_id, "rating": 4}
        res = self.client.post(RATINGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        rating = Ratings.objects.get(id=res.data["id"])
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.rating, payload["rating"])

    def test_update_rating(self):
        """
        Test updating a rating.
        """
        rating = create_rating(user=self.user, movie=self.movie, rating_value=3)

        payload = {"rating": 4}
        url = detail_url(rating.id)
        res = self.client.patch(url, payload)
        rating.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(rating.rating, payload["rating"])

    def test_delete_rating(self):
        """
        Test deleting a rating.
        """

        rating = create_rating(user=self.user, movie=self.movie, rating_value=3)
        url = detail_url(rating.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ratings.objects.filter(id=rating.id).exists())

    def test_rating_limited_to_user(self):
        """
        Test that only ratings for the authenticated user are returned.
        """

        other_user = get_user_model().objects.create_user(
            email="other@example.com", password="testpass123"
        )
        create_rating(user=other_user, movie=self.movie, rating_value=4)
        rating = create_rating(user=self.user, movie=self.movie, rating_value=5)
        res = self.client.get(RATINGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(float(res.data["results"][0]["rating"]), rating.rating)

    def test_unauthorized_rating_update(self):
        """
        Test that a user cannot
        update another user's rating.
        """

        other_user = get_user_model().objects.create_user(
            email="other@example.com", password="testpass123"
        )
        rating = create_rating(user=other_user, movie=self.movie, rating_value=3)
        payload = {"rating": 5}
        url = detail_url(rating.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_rating_delete(self):
        """
        Test that a user cannot
        delete another user's rating.
        """

        other_user = get_user_model().objects.create_user(
            email="other@example.com", password="testpass123"
        )
        rating = create_rating(user=other_user, movie=self.movie, rating_value=3)
        url = detail_url(rating.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
