"""
This module contains ratings views.
"""

from rest_framework import filters, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from core.models import Ratings
from ratings import serializer


class RatingPagination(PageNumberPagination):
    page_size = 10  # Set the number of items per page


class RatingViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    Manage ratings in the database.
    """

    serializer_class = serializer.RatingDetailSerializer
    queryset = Ratings.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["movie__title"]
    ordering_fields = ["id", "rating", "created_at"]
    pagination_class = RatingPagination

    def get_queryset(self):
        """
        Return ratings for the current authenticated user only.
        """
        movie_id = self.request.query_params.get("movie_id")
        queryset = self.queryset.filter(user=self.request.user).order_by("-created_at")
        if movie_id:
            queryset = queryset.filter(movie__id=movie_id)
        return queryset

    def get_serializer_class(self):
        """
        Return appropriate serializer class.
        """
        if self.action == "retrieve":
            return serializer.RatingDetailSerializer  # Serializer for detailed view
        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new rating.
        """

        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Update a rating. Only the owner can update.
        """

        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to edit this rating.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a rating. Only the owner can update.
        """

        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to edit this rating.")
        return super().partial_update(request, *args, **kwargs)
