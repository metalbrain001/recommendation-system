from django.core.management.base import BaseCommand
from core.recommender import RecommenderSystem


class Command(BaseCommand):
    help = "Train and save recommendation models"

    def handle(self, *args, **kwargs):
        recommender = RecommenderSystem()
        self.stdout.write("Training content-based model...")
        recommender.train_and_save_content_based_model()
        self.stdout.write(self.style.SUCCESS("Content-based model trained and saved."))

        self.stdout.write("Training collaborative filtering model...")
        recommender.train_and_save_collaborative_model()
        self.stdout.write(
            self.style.SUCCESS("Collaborative filtering model trained and saved.")
        )
