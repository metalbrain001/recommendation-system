"""
Views for the movies app.
"""

from rest_framework import filters
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from core.models import Movie
from movie import serializer


class MoviePagination(PageNumberPagination):
    page_size = 10


class MovieViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    Manage movies in the database.
    """

    serializer_class = serializer.MovieDetailSerializer
    queryset = Movie.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "genres"]
    ordering_fields = ["id", "title"]
    pagination_class = MoviePagination

    def get_queryset(self):
        """
        Return objects for the current authenticated user only,
        consistently ordered by movie_id.
        """

        genre = self.request.query_params.get("genres")
        queryset = self.queryset.filter(user=self.request.user).order_by("-movie_id")

        if genre:
            queryset = queryset.filter(genres__regex=rf"(^|[|]){genre}([|]|$)")

        return queryset

    def get_serializer_class(self):
        """
        Return appropriate serializer class.
        """

        if self.action == "retrieve":
            return serializer.MovieSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new movie.
        """

        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Update a movie. Only the owner can update.
        """

        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to edit this movie.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a movie.
        Only the owner can update.
        """

        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to edit this movie.")
        return super().partial_update(request, *args, **kwargs)
