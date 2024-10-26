"""
This module contains Tagviewset.
"""

from rest_framework import filters, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from core.models import Tags
from tag import (
    serializer,
)


class TagPagination(PageNumberPagination):
    page_size = 10  # Set items per page


class TagViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    Manage tags in the database.
    """

    serializer_class = serializer.TagDetailSerializer
    queryset = Tags.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "tag",
        "movie__title",
    ]  # Allows searching by tag name or movie title
    ordering_fields = ["id", "tag", "created_at"]
    pagination_class = TagPagination

    def get_queryset(self):
        """
        Return tags for the current authenticated user only.
        """
        movie_id = self.request.query_params.get("movie_id")
        queryset = self.queryset.filter(user=self.request.user).order_by("-id")
        if movie_id:
            queryset = queryset.filter(movie__id=movie_id)
        return queryset

    def get_serializer_class(self):
        """
        Return appropriate serializer class.
        """
        if self.action == "retrieve":
            return serializer.TagDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new tag.
        """

        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Update a tag. Only the owner can update.
        """

        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to edit this tag.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a tag. Only the owner can update.
        """

        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to edit this tag.")
        return super().partial_update(request, *args, **kwargs)
