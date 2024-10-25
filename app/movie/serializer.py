"""
Serializer for movies app
"""

from rest_framework import serializers
from core.models import Movie, UserCollection


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for movie objects
    """

    class Meta:
        model = Movie
        fields = ("movie_id", "title", "genres")
        read_only_fields = ("id", "user")


class MovieDetailSerializer(MovieSerializer):
    """
    Serialize a movie detail
    """

    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields
        read_only_fields = ("id",)


class UserCollectionSerializer(serializers.ModelSerializer):
    """
    Serializer for user collection objects
    """

    class Meta:
        model = UserCollection
        fields = ("id", "name", "movies")
        read_only_fields = ("id", "user")
        depth = 1
