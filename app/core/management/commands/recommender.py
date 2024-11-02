"""
Django management command to run the recommender system
"""

from django.core.management.base import BaseCommand
from core.recomm import RecommenderSystem


class Command(BaseCommand):
    help = "Run the recommender systeand print recommendations"

    def handle(self, *args, **kwargs):
        # Initialize the recommender system
        recommender = RecommenderSystem()

        # Content-based recommendations
        content_recommendations = recommender.content_based_filtering(
            "Jumanji (1995)", top_n=10
        )
        self.stdout.write(self.style.SUCCESS("Content-based recommendations:"))
        for movie in content_recommendations:
            self.stdout.write(f"- {movie}")

        # Collaborative filtering recommendations
        svd_model, _ = recommender.collaborative_filtering()
        collab_recommendations = recommender.recommend_movies(
            user_id=1, svd_model=svd_model, top_n=10
        )
        self.stdout.write(
            self.style.SUCCESS("\nCollaborative filtering recommendations:")
        )
        for movie in collab_recommendations:
            self.stdout.write(f"- {movie}")
