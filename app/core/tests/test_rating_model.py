"""
This module contain test for Rating movies model
"""

from core.models import Ratings
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """
    This class contains test for rating model
    """

    def test_rate_movie(self):
        """
        Test creating a new rating
        """

        user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpass123"
        )

        movie = Ratings.objects.create(
            movie_id=1,
            user=user,
            rating=5
        )

        self.assertEqual(movie.movie_id, 1)
        self.assertEqual(movie.user, user)
        self.assertEqual(movie.rating, 5)
        self.assertEqual(Ratings.objects.count(), 1)

    def test_get_user_rating(self):
        """
        Test getting user rating
        """

        user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpass123"
        )

        rating = Ratings.objects.create(
            movie_id=1,
            user=user,
            rating=5
        )

        self.assertEqual(rating.get_user_rating(), 5)
        self.assertEqual(rating.get_user_rating(), rating.rating)
        self.assertEqual(rating.get_user_rating(), rating.rating)
