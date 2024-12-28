"""
This file contains test for chatbot model.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import ChatHistory


class ModelTests(TestCase):
    """
    Test the chatbot model.
    """

    def test_create_chat_history(self):
        """
        Test creating a new chat history entry.
        """
        user = get_user_model().objects.create_user(
            email="chatbot@example.com",
            password="testpass123",
        )

        chat = ChatHistory.objects.create(
            user=user,
            message="Hello, recommend me a movie.",
            response="Sure, how about Inception?",
        )

        self.assertEqual(chat.message, "Hello, recommend me a movie.")
        self.assertEqual(chat.response, "Sure, how about Inception?")
        self.assertEqual(chat.user, user)

    def test_chat_history_str(self):
        """
        Test the string representation of chat history.
        """
        user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="testpass123",
        )
        chat = ChatHistory.objects.create(
            user=user,
            message="Recommend a movie",
            response="Try The Matrix",
        )
        self.assertEqual(str(chat), f"{user.email}: Recommend a movie")
