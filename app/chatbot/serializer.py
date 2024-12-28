"""
This file contains serializers for chatbot app.
"""

from rest_framework import serializers
from core.models import ChatHistory


class ChatHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for chat history objects.
    """

    class Meta:
        model = ChatHistory
        fields = ["id", "user", "message", "response", "timestamp"]
        read_only_fields = ["id", "timestamp", "user"]


class ChatHistoryDetailSerializer(ChatHistorySerializer):
    """
    Serialize a chat history detail.
    """

    class Meta(ChatHistorySerializer.Meta):
        fields = ChatHistorySerializer.Meta.fields
        read_only_fields = ["id", "timestamp"]
