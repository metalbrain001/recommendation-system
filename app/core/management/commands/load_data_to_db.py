"""
This command Loads MovieLens into the database
"""

from django.core.management.base import BaseCommand
from core.dataset_loader import MovieLensDataLoader


class Command(BaseCommand):
    help = 'Loads MovieLens data into the database'

    def handle(self, *args, **options):
        loader = MovieLensDataLoader(
          path="/app/src/ml-32m/")
        loader.load_data()
        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))
