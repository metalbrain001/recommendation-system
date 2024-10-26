"""
This module contains links urls.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from links.views import LinkViewSet

router = DefaultRouter()
router.register("links", LinkViewSet, basename="link")

app_name = "links"

urlpatterns = [
    path("", include(router.urls)),
]
