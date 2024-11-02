"""
This module contains the views for the recsys app.
"""

from django.db.models import Avg
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

    movies = Movie.objects.annotate(average_rating=Avg("ratings__rating"))[:30]
    for movie in movies:
        if movie.average_rating:
            movie.average_rating = round(movie.average_rating, 1)
    return render(request, "recsys/movies_list.html", {"movies": movies})


def registration_page(request):
    """
    Render the registration page
    """

    form = UserRegistrationForm()
    context = {"form": form}
    return render(request, "recsys/registration.html", context)
