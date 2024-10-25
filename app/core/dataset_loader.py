"""
This module contains the MovieLensDataSet class.
It is used to load the MovieLens data into PostgreSQL.
using bulk_create method.
"""

from datetime import datetime, timezone
import pandas as pd
from core.models import Movie, Ratings, Tags, Links
from django.contrib.auth import get_user_model
from django.db import transaction


def create_user(user_id):
    """
    Create a new user with a
    unique email based on user_id
    """

    User = get_user_model()

    email = f"user_{user_id}@example.com"

    user, created = User.objects.get_or_create(
      email=email,
      default={
        'password': "testpass123"
      },
    )
    return user


class MovieLensDataLoader:
    """
    The MovieLensDataLoader class loads the MovieLens dataset files
    and inserts them into Django models.
    """

    def __init__(self, path=""):
        """
        Initialize the path to the MovieLens dataset files.
        """
        self.path = path

    def load_data(self):
        """
        Loads MovieLens dataset files and inserts them into Django models.
        """
        try:
            movies_df = pd.read_csv(f"{self.path}movies.csv")
            ratings_df = pd.read_csv(f"{self.path}ratings.csv")

            print("Files loaded successfully!")

            # Insert movies into the database
            self.load_movies(movies_df)
            self.load_ratings(ratings_df)

        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None

    @transaction.atomic
    def load_movies(self, movies_df):
        """
        Insert movies data into the database.
        """
        # Filter out movies that already exist in the database
        existing_movies = set(Movie.objects.values_list("movie_id", flat=True))
        movies_df = movies_df[~movies_df["movieId"].isin(existing_movies)]

        movie_objects = [
            Movie(
                movie_id=row["movieId"],  # int64
                title=row["title"],
                genres=row["genres"]
            )
            for index, row in movies_df.iterrows()
        ]

        # Bulk insert the movies into the database
        Movie.objects.bulk_create(movie_objects, batch_size=5000)
        print(f"{len(movie_objects)} movies loaded into the database.")

    @transaction.atomic
    def load_ratings(self, ratings_df):
        """
        Insert ratings data into the database.
        """
        # Preload Movies and Users
        movie_map = {movie.movie_id: movie for movie in Movie.objects.all()}
        user_map = {user.id: user for user in get_user_model().objects.all()}

        # Filter out ratings that already exist in the database
        existing_ratings = set(Ratings.objects.values_list(
          "user_id", "movie_id"))

        rating_objects = []
        for index, row in ratings_df.iterrows():
            # Ensure no duplicates are inserted
            if (row["userId"], row["movieId"]) not in existing_ratings:
                # Convert timestamp to a Python datetime object
                timestamp = datetime.fromtimestamp(
                  row["timestamp"], timezone.utc
                  ) if row["timestamp"] > 0 else None

                rating = Ratings(
                    user=user_map.get(row["userId"]),
                    movie=movie_map.get(row["movieId"]),
                    rating=row["rating"],
                    timestamp=timestamp,
                )
                rating_objects.append(rating)

            # Optional: Log progress for large datasets
            if index % 10000 == 0:
                print(f"Processed {index} ratings...")

        # Bulk insert the ratings
        Ratings.objects.bulk_create(rating_objects, batch_size=5000)
        print(f"{len(rating_objects)} ratings loaded into the database.")

    @transaction.atomic
    def load_tags(self, tags_df):
        """
        Insert tags data into the database.
        """

        # Preload Movies and Users
        movie_map = {movie.movie_id: movie for movie in Movie.objects.all()}
        user_map = {user.id: user for user in get_user_model().objects.all()}

        # Filter out tags that already exist in the database
        existing_tags = set(Tags.objects.values_list(
          "user_id", "movie_id"))

        tag_objects = []
        for index, row in tags_df.iterrows():
            # Ensure no duplicates are inserted
            if (row["userId"], row["movieId"]) not in existing_tags:
                # Convert timestamp to a Python datetime object
                timestamp = datetime.fromtimestamp(
                  row["timestamp"], timezone.utc
                  ) if row["timestamp"] > 0 else None

                tag = Tags(
                    user=user_map.get(row["userId"]),
                    movie=movie_map.get(row["movieId"]),
                    tag=row["tag"],
                    timestamp=timestamp,
                )
                tag_objects.append(tag)

            if index % 10000 == 0:
                print(f"Processed {index} tags...")

        # Bulk insert the tags
        Tags.objects.bulk_create(tag_objects, batch_size=5000)
        print(f"{len(tag_objects)} tags loaded into the database.")

    @transaction.atomic
    def load_links(self, links_df):
        """
        Insert links data into the database.
        """
        # Filter out links that already exist in the database
        existing_links = set(Links.objects.values_list("movie_id", flat=True))
        links_df = links_df[~links_df["movieId"].isin(existing_links)]

        link_objects = [
            Links(
                movie_id=row["movieId"],
                imdb_id=row["imdbId"],
                tmdb_id=row["tmdbId"]
            )
            for index, row in links_df.iterrows()
        ]

        # Bulk insert the links into the database
        Links.objects.bulk_create(link_objects, batch_size=5000)
        print(f"{len(link_objects)} links loaded into the database.")
