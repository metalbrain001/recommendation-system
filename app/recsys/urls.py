"""
This module contains all route and
view functions for the app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # path("", home),
    path("", views.home, name=""),
    path("movies_list/", views.movies_list, name="movies_list"),
]
