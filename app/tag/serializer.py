"""
This module contains tag serializers.
"""

from rest_framework import serializers
from core.models import Tags, Movie


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for tag objects
    """

    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Tags
        fields = ("id", "movie", "tag", "timestamp")
        read_only_fields = ("id", "user", "timestamp")


class TagDetailSerializer(TagSerializer):
    """
    Serialize a tag detail
    """

    class Meta(TagSerializer.Meta):
        fields = TagSerializer.Meta.fields + ("movie", "user")
        read_only_fields = ("id", "user", "timestamp", "movie")
