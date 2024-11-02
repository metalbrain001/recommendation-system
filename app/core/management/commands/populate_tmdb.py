# movies/management/commands/populate_movie_tmdb_ids.py

from django.core.management.base import BaseCommand
from core.models import Links


class Command(BaseCommand):
    help = "Populate tmdb_id in Movie model from Links model"

    def handle(self, *args, **kwargs):
        links = Links.objects.exclude(imdb_id=None)

        for link in links:
            movie = link.movie
            if not movie.imdb_id:
                movie.imdb_id = link.imdb_id
                movie.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Updated tmdb_id for: {movie.title}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"TMDB ID already exists for: {movie.title}")
                )
