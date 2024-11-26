"""
This module contains all route and
view functions for the app.
"""

from django.urls import path
from . import views

app_name = "recsys"

urlpatterns = [
    path("", views.home, name="base"),
    path("movies_list/", views.movies_list, name="movies_list"),
    path("movies_search/", views.movies_search, name="movies_search"),
    path("real-time-search/", views.real_time_search, name="real_time_search"),
    path("movies_details/<int:movie_id>/", views.movies_details, name="movies_details"),
    path("register/", views.registration_page, name="register"),
]
