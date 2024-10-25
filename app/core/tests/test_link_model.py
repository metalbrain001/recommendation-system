"""
This module tests the link model.
"""

from django.test import TestCase
from core.models import Links, Movie
from django.contrib.auth import get_user_model


class LinksModelTests(TestCase):
    """
    Tests for the Links model.
    """

    def test_links_creation(self):
        """
        Test that a Links instance can
        be created with movie, imdb_id,
        and tmdb_id.
        """

        user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123"
        )
        movie = Movie.objects.create(
            movie_id=1, title="Sample Movie", genres="Action", user=user
        )

        link = Links.objects.create(movie=movie, imdb_id=123456, tmdb_id=654321.0)

        # Verify the Links instance was created as expected
        self.assertEqual(link.movie, movie)
        self.assertEqual(link.imdb_id, 123456)
        self.assertEqual(link.tmdb_id, 654321.0)
        self.assertEqual(Links.objects.count(), 1)

    def test_get_imdb_id(self):
        """
        Test the get_imdb_id method
        returns the correct IMDB ID.
        """

        user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123"
        )
        movie = Movie.objects.create(
            movie_id=1, title="Sample Movie", genres="Action", user=user
        )

        link = Links.objects.create(movie=movie, imdb_id=123456, tmdb_id=654321.0)
        self.assertEqual(link.get_imdb_id(), 123456)

    def test_get_tmdb_id(self):
        """
        Test the get_tmdb_id method
        returns the correct TMDB ID.
        """
        user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123"
        )
        movie = Movie.objects.create(
            movie_id=1, title="Sample Movie", genres="Action", user=user
        )

        link = Links.objects.create(movie=movie, imdb_id=123456, tmdb_id=654321.0)

        self.assertEqual(link.get_tmdb_id(), 654321.0)

    def test_links_str(self):
        """
        Test the string representation of the Links model.
        """
        user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123"
        )
        movie = Movie.objects.create(
            movie_id=1, title="Sample Movie", genres="Action", user=user
        )

        link = Links.objects.create(movie=movie, imdb_id=123456, tmdb_id=654321.0)
        self.assertEqual(str(link), "Sample Movie - IMDB: 123456, TMDB: 654321.0")
