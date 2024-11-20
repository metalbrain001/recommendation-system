"""
This module contains all route and
view functions for the app.
"""

from django.urls import path
from . import views

app_name = "recsys"

urlpatterns = [
    path("", views.home, name=""),
    path("movies_list/", views.movies_list, name="movies_list"),
    path("movies_search/", views.movies_search, name="movies_search"),
    path("register/", views.registration_page, name="register"),
]
