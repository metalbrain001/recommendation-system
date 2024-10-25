"""
Movie URL patterns.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from movie import views

router = DefaultRouter()
router.register("movie", views.MovieViewSet)

app_name = "movie"

urlpatterns = [
    path("", include(router.urls)),
]
