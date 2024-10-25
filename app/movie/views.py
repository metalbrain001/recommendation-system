"""
Views for the movies app.
"""

from rest_framework import filters
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from core.models import Movie
from movie import serializer


class MoviePagination(PageNumberPagination):
    page_size = 10  # Number of items per page


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
        Return objects for the current authenticated user only.
        """

        return self.queryset.filter(
          user=self.request.user).order_by("-movie_id")

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
