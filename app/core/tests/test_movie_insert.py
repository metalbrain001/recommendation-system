"""
This module Test Movie Insertion
"""

from django.test import TestCase
from core.models import Movie
from django.contrib.auth import get_user_model


class MovieModelTest(TestCase):
    """
    Test bulk insertion of movies.
    """

    def test_movie_bulk_insert(self):
        """
        Test bulk insert of movies into the Movie model.
        """

        user = get_user_model().objects.create_user(
              "test7@example.com",
              "testpass"
        )

        # Define the movie data to be inserted
        movie_data = [
            Movie(
                  movie_id=1,
                  title="Test Movie 1",
                  genres="Action|Adventure",
                  user=user),
            Movie(
                movie_id=2,
                title="Test Movie 2",
                genres="Drama|Romance",
                user=user
                ),
            Movie(
                movie_id=3,
                title="Test Movie 3",
                genres="Comedy|Drama",
                user=user),
        ]

        # Perform bulk insert of movies
        Movie.objects.bulk_create(movie_data)

        # Assert that 3 movies were inserted
        self.assertEqual(Movie.objects.count(), 3)

        # Verify that the first movie's data is correct
        movie = Movie.objects.get(movie_id=1)
        self.assertEqual(movie.title, "Test Movie 1")
        self.assertEqual(movie.genres, "Action|Adventure")

        # Verify that the second movie's data is correct
        movie = Movie.objects.get(movie_id=2)
        self.assertEqual(movie.title, "Test Movie 2")
        self.assertEqual(movie.genres, "Drama|Romance")

        # Verify that the third movie's data is correct
        movie = Movie.objects.get(movie_id=3)
        self.assertEqual(movie.title, "Test Movie 3")
        self.assertEqual(movie.genres, "Comedy|Drama")
