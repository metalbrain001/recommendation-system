"""
This module contains the views for the recsys app.
"""

from django.utils.timezone import now
from datetime import timedelta
from django.conf import settings
from django.db.models import Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
import requests
from core.models import Movie
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
import logging

logger = logging.getLogger(__name__)


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

    # Check if the request is an AJAX request
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # Render only the partial template for AJAX requests
        return render(request, "recsys/movies_list.html", {"movies": page_obj})

    return render(request, "recsys/movies_list.html", {"movies": page_obj})


def top_rated_movies(request):
    """
    Return the top rated movies as JSON
    for API calls or render HTML for regular requests.
    """

    movies = Movie.objects.annotate(average_rating=Avg("ratings__rating"))[:8]

    # Round the average ratings
    for movie in movies:
        if movie.average_rating:
            movie.average_rating = round(movie.average_rating, 1)

    # Handle JSON requests (e.g., from fetch)
    if (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or request.content_type == "application/json"
    ):
        movies_data = [
            {
                "movie_id": movie.movie_id,
                "title": movie.title,
                "poster_url": movie.poster_url,
                "average_rating": movie.average_rating or "N/A",
            }
            for movie in movies
        ]
        return JsonResponse(movies_data, safe=False)

    # Handle standard HTML requests
    return render(request, "recsys/top_rated_movies.html", {"movies": movies})


def recent_release_movies(request):
    """
    Return the recent release movies as JSON
    for API calls or render HTML for regular requests.
    """

    recent_threshold = now() - timedelta(days=5 * 365)

    movies = Movie.objects.filter(
        poster_url__isnull=False, created_at__gte=recent_threshold
    ).order_by("-created_at")[:8]

    # movies = Movie.objects.filter(poster_url__isnull=False).order_by("-created_at")[:8]

    # Log movies with missing posters
    for movie in movies:
        if not movie.poster_url:
            logger.warning(
                f"Missing poster for movie: {movie.title} (ID: {movie.movie_id})"
            )

    # Handle JSON requests (e.g., from fetch)
    if (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or request.content_type == "application/json"
    ):
        movies_data = [
            {
                "movie_id": movie.movie_id,
                "title": movie.title,
                "poster_url": movie.poster_url
                or "https://via.placeholder.com/500x750?text=No+Poster+Available",
                "release_date": movie.created_at.strftime("%Y-%m-%d"),
            }
            for movie in movies
        ]
        return JsonResponse(movies_data, safe=False)

    # Handle standard HTML requests
    return render(request, "recsys/recent_release_movies.html", {"movies": movies})


def movies_by_genre(request, genre):
    """
    Fetch movies by genre for API requests
    or render HTML for a specific genre.
    """

    movies = Movie.objects.filter(
        genres__icontains=genre,  # Case-insensitive search
        poster_url__isnull=False,
    ).order_by("-created_at")[
        :8
    ]  # Limit to 8 movies

    # Handle JSON requests (e.g., from AJAX or fetch API)
    if (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or request.content_type == "application/json"
    ):
        movies_data = [
            {
                "movie_id": movie.movie_id,
                "title": movie.title,
                "poster_url": movie.poster_url,
                "genre": movie.genres,
                "release_date": movie.created_at.strftime("%Y-%m-%d"),
            }
            for movie in movies
        ]
        return JsonResponse(movies_data, safe=False)

    # Render HTML for regular requests
    return render(
        request,
        "recsys/movies_by_genre.html",
        {"movies": movies, "genre": genre},
    )


def genre_movies_full_page(request, genre):
    """
    Fetch all movies by genre for a full-page display with pagination.
    """
    movies = Movie.objects.filter(
        genres__icontains=genre,
        poster_url__isnull=False,
    ).order_by("-created_at")

    # Handle JSON requests for API
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        page = request.GET.get("page", 1)
        paginator = Paginator(movies, 20)  # 20 movies per page
        try:
            paginated_movies = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            paginated_movies = paginator.page(1)

        # Serialize movies using object_list
        movies_data = [
            {
                "movie_id": movie.movie_id,
                "title": movie.title,
                "poster_url": movie.poster_url,
                "genres": movie.genres,
                "release_date": movie.created_at.strftime("%Y-%m-%d"),
                "average_rating": (
                    movie.average_rating if hasattr(movie, "average_rating") else "N/A"
                ),
            }
            for movie in paginated_movies.object_list
        ]

        return JsonResponse(
            {
                "movies": movies_data,
                "page": paginated_movies.number,
                "total_pages": paginator.num_pages,
            }
        )

    # Handle HTML rendering for full-page view
    if not movies.exists():
        raise Http404(f"No movies found for genre: {genre}")

    return render(request, "recsys/genre_movies.html", {"genre": genre})


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

    # If request is AJAX, return JSON
    if (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or request.content_type == "application/json"
    ):
        return JsonResponse(
            {
                "movie": {
                    "title": movie.title,
                    "poster_url": movie.poster_url,
                    "genres": movie_details.get("genres", []),
                    "release_date": movie_details.get("release_date"),
                    "runtime": movie_details.get("runtime"),
                    "budget": movie_details.get("budget"),
                    "vote_average": movie_details.get("vote_average"),
                    "overview": movie_details.get("overview"),
                },
                "trailer_url": trailer_url,
            }
        )

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

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect("recsys:login")
    else:
        email = request.GET.get("email", "")
        form = UserRegistrationForm(initial={"email": email})

    context = {"form": form}
    return render(request, "recsys/registration.html", context)


def login_page(request):
    """
    Handle AJAX and standard login requests.
    """
    if request.method == "POST":
        # Detect if the request is AJAX
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        # Extract email and password from POST data
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)

            # JSON response for AJAX
            if is_ajax:
                return JsonResponse(
                    {"message": "Login successful!", "redirect_url": "/dashboard/"}
                )

            # Redirect for standard form submission
            return redirect("/dashboard/")
        else:
            # Handle login failure
            if is_ajax:
                return JsonResponse({"error": "Invalid email or password."}, status=400)
            else:
                messages.error(request, "Invalid email or password.")

    # Render login page for GET or failed POST
    return render(request, "recsys/login.html", {"form": LoginForm()})


@csrf_protect
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("recsys:base")
    return redirect("recsys:dashboard")


@login_required
def dashboard(request):
    """
    Render the dashboard or return JSON data.
    """

    # Return JSON data if requested
    if request.headers.get("Accept") == "application/json":
        return JsonResponse({"message": f"Welcome back, {request.user}!"})

    # Otherwise, render the dashboard template
    return render(request, "recsys/dashboard.html", {"user": request.user})
