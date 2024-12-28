"""
This module contains the views for the chatbot app.
"""

import sys
import os
from rest_framework.response import Response
import openai
from rest_framework import viewsets, mixins
from rest_framework import filters
from core.models import ChatHistory
from chatbot import serializer
from app.utils import get_openai_key
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from chatbot.utils import load_trained_recommender


class ChatbotPagination(PageNumberPagination):
    page_size = 10  # Set the number of items per page


# Set OpenAI API key
openai.api_key = get_openai_key()


class ChatbotViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A simple ViewSet for handling chatbot interactions.
    """

    serializer_class = serializer.ChatHistoryDetailSerializer
    queryset = ChatHistory.objects.all()
    pagination_class = ChatbotPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        """
        Restrict the queryset to the authenticated user's entries.
        Allow filtering by search keyword.
        """

        queryset = self.queryset.filter(user=self.request.user).order_by("-timestamp")
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                message__icontains=search
            )  # Apply case-insensitive search filter
        return queryset

    def get_serializer_class(self):
        """
        Return appropriate serializer class.
        """

        if self.action == "retrieve":
            return serializer.ChatHistorySerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new chat history entry.
        """

        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Handle PUT requests for chatbot interactions.
        """

        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to edit this movie.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially updating a chat history entry.
        """

        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to edit this chat.")
        return super().partial_update(request, *args, **kwargs)

    def create(self, request):

        if not request.user.is_authenticated:
            return Response(
                {"error": "You must be logged in to access this feature."}, status=401
            )

        movie_title = request.data.get("movie_title", "").strip()
        user_id = request.user.id if request.user.is_authenticated else None

        if not movie_title:
            return Response(
                {"error": "The 'movie_title' field is required."}, status=400
            )

        try:

            # Load the trained recommender system
            recommender = load_trained_recommender()

            # Content-based recommendations
            content_recommendations = recommender.content_based_filtering(
                movie_title, top_n=5
            )

            # Collaborative recommendations (if user is authenticated)
            collaborative_recommendations = []
            if user_id:
                svd_model, _ = recommender.collaborative_filtering()
                collaborative_recommendations = recommender.recommend_movies(
                    user_id=user_id, svd_model=svd_model, top_n=5
                )

            # Create chat history
            chat = ChatHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                message=movie_title,
                response=", ".join(content_recommendations[:5]),
            )

            # Serialize and return response
            serialized_chat = serializer.ChatHistorySerializer(chat)
            respose_data = {
                "chat_history": serialized_chat.data,
                "content_recommendations": content_recommendations,
                "collaborative_recommendations": collaborative_recommendations,
            }
            return Response(respose_data, status=201)

        except openai.OpenAIError as e:
            return Response(
                {"error": f"An error occurred with the OpenAI API: {str(e)}"},
                status=400,
            )

        except FileNotFoundError as e:
            return Response(
                {"error": f"An error occurred loading the trained models: {str(e)}"},
                status=500,
            )

        except ValueError as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=400)

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"}, status=500
            )
