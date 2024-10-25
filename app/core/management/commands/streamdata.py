"""
This command streams data into the database
"""

from django.core.management.base import BaseCommand
from core.stream import StreamRatingToDb


class Command(BaseCommand):
    help = 'Streams MovieLens data into the database'

    def handle(self, *args, **options):
        streamer = StreamRatingToDb(
          path="/home/babsdevsys/recommendation-system/app/src/ml-32m/")
        streamer.stream_ratings_to_db()
        self.stdout.write(self.style.SUCCESS('Successfully streamed data'))
