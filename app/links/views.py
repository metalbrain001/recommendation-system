"""
This module contains views for links
"""

from rest_framework import filters, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from core.models import Links
from links import serializer


class LinkPagination(PageNumberPagination):
    page_size = 10  # Set items per page


class LinkViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    Manage links in the database.
    """

    serializer_class = serializer.LinkDetailSerializer
    queryset = Links.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "movie__title",
        "imdb_id",
        "tmdb_id",
    ]
    ordering_fields = ["id", "imdb_id", "tmdb_id"]
    pagination_class = LinkPagination

    def get_queryset(self):
        """
        Return links for the current
        authenticated user only.
        """

        movie_id = self.request.query_params.get("movie_id")
        queryset = self.queryset.filter(movie__user=self.request.user).order_by("-id")

        if movie_id:
            queryset = queryset.filter(movie__id=movie_id)

        return queryset

    def get_serializer_class(self):
        """
        Return appropriate serializer class.
        """

        if self.action == "retrieve":
            return serializer.LinkDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new link.
        """
        serializer.save()

    def update(self, request, *args, **kwargs):
        """
        Update a link. Only the owner can update.
        """
        instance = self.get_object()
        if instance.movie.user != request.user:
            raise PermissionDenied("You do not have permission to edit this link.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a link. Only the owner can update.
        """
        instance = self.get_object()
        if instance.movie.user != request.user:
            raise PermissionDenied("You do not have permission to edit this link.")
        return super().partial_update(request, *args, **kwargs)
