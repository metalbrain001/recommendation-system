"""
This file contains test for chatbot API.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from chatbot.serializer import ChatHistorySerializer
from core.models import ChatHistory


CHAT_BOT_URL = reverse("chatbot:chatbot-list")


def detail_url(chat_id):
    """
    Return chatbot detail URL.
    """

    return reverse("chatbot:chatbot-detail", args=[chat_id])


def create_chat_history(user, **params):
    """
    Helper function to create a new chat history.
    """

    defaults = {
        "message": "Hello, recommend me a movie.",
        "response": "Sure, how about Inception?",
    }
    defaults.update(params)
    return ChatHistory.objects.create(user=user, **defaults)


def create_user(**params):
    """
    Helper function to create a new user.
    """

    return get_user_model().objects.create_user(**params)


class PublicChatBotApiTests(TestCase):
    """
    Test the chatbot API (public).
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that authentication is
        required for retrieving chat history.
        """

        res = self.client.get(CHAT_BOT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateChatBotApiTests(TestCase):
    """
    Test the chatbot API (private).
    """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="test@example.com", password="testpass123")
        self.client.force_authenticate(self.user)

    def test_create_chat_history_successful(self):
        """
        Test creating a new chat history entry.
        """

        payload = {
            "movie_title": "Tom and Huck (1995)",
        }

        res = self.client.post(CHAT_BOT_URL, payload)
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual("chat_history" in res.data, True)
        self.assertEqual("content_recommendations" in res.data, True)
        self.assertEqual("collaborative_recommendations" in res.data, True)
        exists = ChatHistory.objects.filter(
            user=self.user, message=payload["movie_title"]
        ).exists()
        self.assertTrue(exists)

    def test_retrieve_chat_history(self):
        """
        Test retrieving chat history.
        """

        ChatHistory.objects.create(
            user=self.user,
            message="Recommend an action movie.",
            response="Sure, how about Inception?",
        )
        ChatHistory.objects.create(
            user=self.user,
            message="What about a comedy?",
            response="Sure, how about Inception?",
        )

        res = self.client.get(CHAT_BOT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 2)  # Check total count
        self.assertEqual(
            len(res.data["results"]), 2
        )  # Check number of items in results

        # Verify data matches the expected response
        self.assertEqual(res.data["results"][0]["message"], "What about a comedy?")
        self.assertEqual(
            res.data["results"][1]["message"], "Recommend an action movie."
        )

    def test_chat_history_limited_to_user(self):
        """
        Test that chat history is limited to user.
        """

        user2 = get_user_model().objects.create_user("other@example.com", "password123")
        ChatHistory.objects.create(
            user=user2, message="User2 message.", response="User2 response."
        )

        ChatHistory.objects.create(
            user=self.user, message="User1 message.", response="User1 response."
        )

        res = self.client.get(CHAT_BOT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)  # Only one chat for self.user
        self.assertEqual(res.data["results"][0]["message"], "User1 message.")

    def test_partial_update_chat_history(self):
        """
        Test updating a chat
        history entry with PATCH.
        """

        chat = create_chat_history(user=self.user, message="Old message.")
        payload = {"message": "Updated message."}
        url = detail_url(chat.id)
        res = self.client.patch(url, payload)
        chat.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(chat.message, payload["message"])

    def test_full_update_chat_history(self):
        """
        Test updating a chat
        history entry with PUT.
        """

        chat = create_chat_history(
            user=self.user, message="Old message.", response="Old response."
        )
        payload = {
            "message": "Updated message.",
            "response": "Updated response.",
            "user": self.user.id,
        }
        url = detail_url(chat.id)
        res = self.client.put(url, payload)
        print(res.data)
        chat.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(chat.message, payload["message"])
        self.assertEqual(chat.response, payload["response"])

    def test_delete_chat_history(self):
        """
        Test deleting a chat history entry.
        """

        chat = create_chat_history(user=self.user)
        url = detail_url(chat.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ChatHistory.objects.filter(id=chat.id).exists())

    def test_unauthorized_chat_update(self):
        """
        Test that a chat history entry
        cannot be updated by another user.
        """

        user2 = create_user(email="otheruser@example.com", password="password123")

        chat = create_chat_history(user=user2, message="Not yours.")
        payload = {"message": "Hacked message."}
        url = detail_url(chat.id)
        res = self.client.patch(url, payload)
        chat.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(chat.message, "Not yours.")

    def test_unauthorized_chat_delete(self):
        """
        Test that a chat history entry
        cannot be deleted by another user.
        """

        user2 = create_user(email="otheruser@example.com", password="password123")

        chat = create_chat_history(user=user2)
        url = detail_url(chat.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(ChatHistory.objects.filter(id=chat.id).exists())

    def test_filter_chat_history_by_keyword(self):
        """
        Test filtering chat history
        by a keyword in the message.
        """

        create_chat_history(
            user=self.user,
            message="Recommend an action movie.",
            response="Sure, how about Inception?",
        )

        create_chat_history(
            user=self.user,
            message="What about a comedy?",
            response="Sure, how about Inception?",
        )

        res = self.client.get(CHAT_BOT_URL, {"search": "action"})
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)  # Only one result matches
        self.assertEqual(
            res.data["results"][0]["message"], "Recommend an action movie."
        )
