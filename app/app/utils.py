# movies/utils.py
import requests
from django.conf import settings
import pickle


def fetch_movie_poster(imdb_id):
    """
    Fetches the poster URL for a movie using its TMDB ID.
    """

    url = f"https://api.themoviedb.org/3/movie/{int(imdb_id)}"
    params = {"api_key": settings.TMDB_API_KEY}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Construct the full URL for the poster image
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for TMDB ID {imdb_id}: {e}")
        return None


def get_openai_key():
    """
    Retrieves the OpenAI API key securely.
    """

    try:
        params = {"api_key": settings.OPEN_AI_API_KEY}
        if not params["api_key"]:
            raise ValueError("OpenAI API key is not set in the environment variables.")
        return params
    except Exception as e:
        print(f"Error retrieving OpenAI API key: {e}")
        return None


def load_models():
    """
    Load saved models from the paths specified in settings.
    """

    content_model_path = settings.RECOMMENDER_CONTENT_MODEL_PATH
    collaborative_model_path = settings.RECOMMENDER_COLLABORATIVE_MODEL_PATH

    # Load content-based model
    with open(content_model_path, "rb") as f:
        content_based_model = pickle.load(f)

    # Load collaborative filtering model
    with open(collaborative_model_path, "rb") as f:
        collaborative_model = pickle.load(f)

    return content_based_model, collaborative_model
