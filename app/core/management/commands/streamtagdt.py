"""
This command streams tag data into the database
"""

from django.core.management.base import BaseCommand
from core.streamtag import StreamTagToDb


class Command(BaseCommand):
    help = 'Streams MovieLens tag data into the database'

    def handle(self, *args, **options):
        streamer = StreamTagToDb(
          path="/home/babsdevsys/recommendation-system/app/src/ml-32m/")
        streamer.stream_tags_to_db()
        self.stdout.write(self.style.SUCCESS('Successfully streamed tag data'))
