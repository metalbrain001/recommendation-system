"""
This module contains urls for ratings.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from ratings import views

router = DefaultRouter()

router.register("ratings", views.RatingViewSet)

app_name = "ratings"

urlpatterns = [
    path("", include(router.urls)),
]
