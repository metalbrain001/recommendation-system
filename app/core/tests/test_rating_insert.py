from django.contrib.auth import get_user_model
from django.test import TestCase
from core.models import Ratings, Movie


class RatingModelTest(TestCase):

    def test_rating_bulk_insert(self):
        """
        Test bulk insert of ratings.
        """

        user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpass123"
        )
        movie = Movie.objects.create(
          movie_id=1,
          title="Test Movie",
          user=user
        )

        ratings = [
            Ratings(user=user, movie=movie, rating=5.0),
        ]

        Ratings.objects.bulk_create(ratings)

        self.assertEqual(Ratings.objects.count(), 1)
        for rating in Ratings.objects.all():
            self.assertEqual(rating.movie, movie)
            self.assertIn(rating.rating, [5.0])
