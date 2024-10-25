from django.test import TestCase
from core.models import Links, Movie
from django.contrib.auth import get_user_model


class LinksModelTest(TestCase):
    """
    Test bulk insertion of links.
    """

    def test_link_bulk_insert(self):
        """
        Test bulk insert of links into the Links model.
        """

        user = get_user_model().objects.create_user(
            "other@cample.com",
            "testpass"
        )

        Movie.objects.create(
            movie_id=1,
            title="Test Movie",
            genres="Action",
            user=user
            )
        Movie.objects.create(
            movie_id=2,
            title="Test Movie 2",
            genres="Comedy",
            user=user
            )
        Movie.objects.create(
            movie_id=3,
            title="Test Movie 3",
            genres="Drama",
            user=user
            )

        # Define the links data to be inserted
        link_data = [
            Links(movie_id=1, imdb_id=114709, tmdb_id=862.0),
            Links(movie_id=2, imdb_id=113497, tmdb_id=8844.0),
            Links(movie_id=3, imdb_id=113228, tmdb_id=15602.0),
        ]

        # Perform bulk insert of links
        Links.objects.bulk_create(link_data)

        # Assert that the links were inserted correctly
        self.assertEqual(Links.objects.count(), 3)

        # Verify that the first link's data is correct
        link = Links.objects.get(movie_id=1, imdb_id=114709, tmdb_id=862)

        self.assertEqual(link.imdb_id, 114709)
        self.assertEqual(link.tmdb_id, 862.0)
