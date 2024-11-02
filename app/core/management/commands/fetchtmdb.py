"""
Fetch and save poster images for movies based on imdb_id
"""

import time
import requests
from requests.exceptions import RequestException
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Movie


def fetch_with_retries(url, params, retries=5, backoff=0.3):
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            if attempt < retries - 1:
                time.sleep(backoff * (2**attempt))  # exponential backoff
            else:
                raise e


class Command(BaseCommand):
    help = "Fetch and save poster images for movies based on imdb_id"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.exclude(imdb_id=None).filter(poster_url__isnull=True)
        print(f"Movies to process: {movies.count()}")

        updated_movies = []

        for movie in movies:
            url = f"https://api.themoviedb.org/3/find/tt{int(movie.imdb_id)}"
            params = {"api_key": settings.TMDB_API_KEY, "external_source": "imdb_id"}

            try:
                data = fetch_with_retries(url, params)
                if data["movie_results"]:
                    movie_data = data["movie_results"][0]
                    poster_path = movie_data.get("poster_path")
                    print(f"Starting with {movies.count()} movies without posters")

                    if poster_path and not movie.poster_url:
                        movie.poster_url = (
                            f"https://image.tmdb.org/t/p/w500{poster_path}"
                        )
                        updated_movies.append(movie)

                        self.stdout.write(
                            self.style.SUCCESS(f"Fetched poster for: {movie.title}")
                        )

                time.sleep(0.2)

            except RequestException as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error fetching poster for {movie.title} (IMDb ID: {movie.imdb_id}): {e}"
                    )
                )

        if updated_movies:
            Movie.objects.bulk_update(updated_movies, ["poster_url"])
            self.stdout.write(self.style.SUCCESS("Updated poster URLs in batch"))
