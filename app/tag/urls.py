"""
This module contains urls for tags.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from tag import views

router = DefaultRouter()
router.register("tag", views.TagViewSet, basename="tag")

app_name = "tag"

urlpatterns = [
    path("", include(router.urls)),
]
