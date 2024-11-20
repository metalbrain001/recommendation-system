"""
This module contains the views for the recsys app.
"""

from django.db.models import Avg
from django.core.paginator import Paginator
from django.shortcuts import render
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


def registration_page(request):
    """
    Render the registration page
    """

    form = UserRegistrationForm()
    context = {"form": form}
    return render(request, "recsys/registration.html", context)
