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
    path("top_rated_movies/", views.top_rated_movies, name="top_rated_movies"),
    path(
        "recent_release_movies/",
        views.recent_release_movies,
        name="recent_release_movies",
    ),
    path("movies_search/", views.movies_search, name="movies_search"),
    path("real-time-search/", views.real_time_search, name="real_time_search"),
    path("movies_details/<int:movie_id>/", views.movies_details, name="movies_details"),
    path("movies_by_genre/<str:genre>/", views.movies_by_genre, name="movies_by_genre"),
    path(
        "genre_movies_full_page/<str:genre>/",
        views.genre_movies_full_page,
        name="genre_movies_full_page",
    ),
    path("register/", views.registration_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_user, name="logout"),
]
