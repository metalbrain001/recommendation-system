"""
This module contains the views for the recsys app.
"""

from django.conf import settings
from django.db.models import Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
import requests
from core.models import Movie
from .forms import UserRegistrationForm


# Create your views here.
def home(request):
    """
    Render the home page
    """

    return render(request, "recsys/base.html")


def movies_list(request):
    """
    Annotate movies with average ratings
    """

    movies = Movie.objects.annotate(average_rating=Avg("ratings__rating"))[:100]

    # Set up Pagination with 10 movies per page
    paginator = Paginator(movies, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    for movie in page_obj:
        if movie.average_rating:
            movie.average_rating = round(movie.average_rating, 1)
    return render(request, "recsys/movies_list.html", {"movies": page_obj})


def movies_search(request):
    """
    Search for movies
    """

    query = request.GET.get("query")
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.all()

    # Set up Pagination with 10 movies per page
    paginator = Paginator(movies, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "recsys/movies_search.html", {"movies": page_obj})


def real_time_search(request):
    """
    Real-time search for movies
    """
    query = request.GET.get("query", "").strip()
    if query:
        movies = Movie.objects.filter(title__icontains=query)[
            :10
        ]  # Limit results to 10
        results = [
            {
                "id": movie.movie_id,
                "title": movie.title,
                "poster_url": (
                    movie.poster_url
                    if movie.poster_url
                    else "/static/default-poster.jpg"
                ),
            }
            for movie in movies
        ]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


def movies_details(request, movie_id):
    """
    Fetch and display the details
    of a movie along with its trailer.
    """

    # Fetch movie details from the database
    movie = Movie.objects.get(movie_id=movie_id)

    # Use tmdb_id if available, otherwise fetch it
    tmdb_id = movie.tmdb_id
    if not tmdb_id:
        TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
        search_params = {
            "api_key": settings.TMDB_API_KEY,
            "query": movie.title,
            "year": movie.created_at.year,  # Optional: Filter by release year
        }
        search_response = requests.get(TMDB_SEARCH_URL, params=search_params)
        if search_response.status_code == 200:
            search_data = search_response.json()
            if search_data["results"]:
                tmdb_id = search_data["results"][0]["id"]  # Use the first search result
                movie.tmdb_id = tmdb_id  # Save to database for future use
                movie.save()
        else:
            return JsonResponse(
                {"error": "Failed to find TMDB ID for the movie."}, status=500
            )

    # Fetch Movie details from TMDB API
    TMDB_MOVIE_URL = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    details_params = {"api_key": settings.TMDB_API_KEY, "language": "en-US"}
    details_response = requests.get(
        TMDB_MOVIE_URL, params=details_params
    )  # Fetch movie details
    movie_details = None

    if details_response.status_code == 200:
        movie_details = details_response.json()
    else:
        return JsonResponse(
            {"error": "Failed to fetch movie details from TMDB."}, status=500
        )

    # Fetch the trailer from TMDB API using the correct tmdb_id
    TMDB_MOVIE_URL = f"https://api.themoviedb.org/3/movie/{tmdb_id}/videos"
    params = {"api_key": settings.TMDB_API_KEY}
    trailer_url = None

    response = requests.get(TMDB_MOVIE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        for video in data.get("results", []):
            if video["type"] == "Trailer" and video["site"] == "YouTube":
                # Generate embed URL
                trailer_url = f"https://www.youtube.com/embed/{video['key']}"
                break

    # Pass data to the template
    context = {
        "movie": movie,
        "movie_details": movie_details,
        "trailer_url": trailer_url,
    }
    return render(request, "recsys/movies_details.html", context)


def fetch_popular_movies(request):
    TMDB_DISCOVER_URL = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "page": request.GET.get("page", 1),
    }

    response = requests.get(TMDB_DISCOVER_URL, params=params)
    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    return JsonResponse({"error": response.text}, status=response.status_code)


def registration_page(request):
    """
    Render the registration page
    """

    form = UserRegistrationForm()
    context = {"form": form}
    return render(request, "recsys/registration.html", context)
