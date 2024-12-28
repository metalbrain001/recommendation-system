import os
from django.conf import settings
from core.recommender import RecommenderSystem


def load_trained_recommender():
    """
    Load the trained recommender system
    """

    content_model_path = "content_model.pkl"
    collaborative_model_path = "collaborative_model.pkl"
    recommender = RecommenderSystem()
    recommender.content_model = recommender.load_content_based_model(content_model_path)
    recommender.svd_model = recommender.load_collaborative_model(
        collaborative_model_path
    )
    return recommender
