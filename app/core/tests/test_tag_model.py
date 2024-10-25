"""
This module tests the tag model.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Tags, Movie


class ModelTests(TestCase):
    """
    Test the tag model.
    """

    def test_tag_movie(self):
        """
        Test creating a new tag.
        """

        user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123"
        )

        movie = Movie.objects.create(
            movie_id=1, title="Sample Movie", genres="Action", user=user
        )

        tag = Tags.objects.create(user=user, movie=movie, tag="Action")

        # Verify the tag was created as expected
        self.assertEqual(tag.user, user)
        self.assertEqual(tag.movie, movie)
        self.assertEqual(tag.tag, "Action")
        self.assertEqual(Tags.objects.count(), 1)

    def test_get_movie_tags(self):
        """
        Test getting movie tags.
        """

        user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123"
        )

        movie = Movie.objects.create(
            movie_id=1, title="Sample Movie", genres="Action", user=user
        )

        tag = Tags.objects.create(user=user, movie=movie, tag="Action")

        self.assertEqual(tag.get_movie_tag(), "Action")
        self.assertEqual(tag.get_movie_tag(), tag.tag)
        self.assertEqual(Tags.objects.count(), 1)
