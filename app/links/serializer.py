"""
This module contains links serializers.
"""

from rest_framework import serializers
from core.models import Links, Movie


class LinkSerializer(serializers.ModelSerializer):
    """
    Serializer for link objects
    """

    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Links
        fields = ("id", "movie", "imdb_id", "tmdb_id")
        read_only_fields = ("id",)


class LinkDetailSerializer(LinkSerializer):
    """
    Serialize a link detail
    """

    class Meta(LinkSerializer.Meta):
        fields = LinkSerializer.Meta.fields + ("movie",)
        read_only_fields = ("id", "movie")
