"""
This module contains ratings serializers.
"""

from rest_framework import serializers
from core.models import Ratings, Movie


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for rating objects
    """

    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Ratings
        fields = ("id", "movie", "rating", "timestamp")
        read_only_fields = ("id", "user", "timestamp")


class RatingDetailSerializer(RatingSerializer):
    """
    Serialize a rating detail
    """

    class Meta(RatingSerializer.Meta):
        fields = RatingSerializer.Meta.fields + ("movie", "user")
        read_only_fields = ("id", "user", "timestamp", "movie")
