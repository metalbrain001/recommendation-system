import requests


class TMDbImageFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_image(self, image_url):
        response = requests.get(image_url)
        return response.content

    def fetch_movie_poster(self, movie_id):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={self.api_key}"
        response = requests.get(url)

        # Handle unsuccessful responses gracefully
        if response.status_code != 200:
            print(f"Error fetching movie {movie_id}: {response.status_code}")
            return None

        data = response.json()

        # Check if 'poster_path' exists in data
        poster_path = data.get("poster_path")
        if poster_path:
            image_url = f"https://image.tmdb.org/t/p/original{poster_path}"
            return image_url  # Return the image URL instead of content for efficiency
        else:
            print(f"No poster path found for movie {movie_id}")
            return None

    def fetch_tv_poster(self, tv_id):
        url = f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={self.api_key}"
        response = requests.get(url)

        # Handle unsuccessful responses gracefully
        if response.status_code != 200:
            print(f"Error fetching TV show {tv_id}: {response.status_code}")
            return None

        data = response.json()

        # Check if 'poster_path' exists in data
        poster_path = data.get("poster_path")
        if poster_path:
            image_url = f"https://image.tmdb.org/t/p/original{poster_path}"
            return image_url  # Return the image URL instead of content for efficiency
        else:
            print(f"No poster path found for TV show {tv_id}")
            return None
