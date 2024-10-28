"""
This module contains the views for the recsys app.
"""

from django.shortcuts import render
from core.models import Movie


# Create your views here.
def home(request):
    return render(request, "recsys/base.html")


def movies_list(request):

    # Query all movies from the database
    movies = Movie.objects.all()[:20]  # You can filter or order as needed
    return render(request, "recsys/movies_list.html", {"movies": movies})
