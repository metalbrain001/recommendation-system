# movies/utils.py
import requests
from django.conf import settings


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
