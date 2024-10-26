"""
This module test the tag API.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tags, Movie
from tag.serializer import (
    TagDetailSerializer,
)


TAGS_URL = reverse("tag:tag-list")


def detail_url(tag_id):
    """
    Return tag detail URL.
    """

    return reverse("tag:tag-detail", args=[tag_id])


def create_movie(user, **params):
    """
    Helper function to create a new movie.
    """

    defaults = {
        "movie_id": 1,
        "title": "Toy Story",
        "genres": "Animation|Children's|Comedy",
    }
    defaults.update(params)
    movie = Movie.objects.create(user=user, **defaults)
    return movie


def create_tag(user, movie, tag="Action"):
    """
    Helper function to
    create a tag for a movie.
    """

    return Tags.objects.create(user=user, movie=movie, tag=tag)


class PublicTagApiTests(TestCase):
    """
    Test the publicly available tags API.
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that authentication is
        required for retrieving tags.
        """

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTests(TestCase):
    """
    Test the private tags API.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "tag@example.com", "testpass123"
        )
        self.client.force_authenticate(self.user)
        self.movie = create_movie(user=self.user)

    def test_list_tags(self):
        """
        Test retrieving a list of tags.
        """

        # Use unique movie_id values to avoid conflicts
        movie1 = create_movie(user=self.user, movie_id=300, title="Movie 1")
        movie2 = create_movie(user=self.user, movie_id=200, title="Movie 2")

        create_tag(user=self.user, movie=movie1, tag="Tag 1")
        create_tag(user=self.user, movie=movie2, tag="Tag 2")

        res = self.client.get(TAGS_URL)
        tags = Tags.objects.all().order_by("-id")
        serializer = TagDetailSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_tags_limited_to_user(self):
        """
        Test list of tags returned are for
        the authenticated user.
        """

        user2 = get_user_model().objects.create_user("tag1@example.com", "testpass123")

        # Use unique movie_id values to avoid conflicts
        movie1 = create_movie(user=self.user, movie_id=300, title="Movie 1")
        movie2 = create_movie(user=user2, movie_id=200, title="Movie 2")

        create_tag(user=self.user, movie=movie1, tag="Tag 1")
        create_tag(user=user2, movie=movie2, tag="Tag 2")

        res = self.client.get(TAGS_URL)
        tags = Tags.objects.filter(user=self.user)
        serializer = TagDetailSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_create_tag_successful(self):
        """
        Test creating a new tag.
        """

        payload = {"movie": self.movie.movie_id, "tag": "New Tag"}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        tag = Tags.objects.get(id=res.data["id"])
        self.assertEqual(tag.user, self.user)
        self.assertEqual(tag.tag, payload["tag"])

    def test_create_tag_invalid(self):
        """
        Test creating a new tag with invalid payload.
        """

        payload = {"movie": "", "tag": ""}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("movie", res.data)
        self.assertIn("tag", res.data)

    def test_retrieve_tag_detail(self):
        """
        Test viewing a tag detail.
        """

        tag = create_tag(user=self.user, movie=self.movie, tag="Test Tag")
        url = detail_url(tag.id)
        res = self.client.get(url)
        serializer = TagDetailSerializer(tag)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_tag(self):
        """
        Test updating a tag.
        """

        tag = create_tag(user=self.user, movie=self.movie, tag="Initial Tag")
        payload = {"tag": "Updated Tag"}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)
        tag.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(tag.tag, payload["tag"])

    def test_delete_tag(self):
        """
        Test deleting a tag.
        """

        tag = create_tag(user=self.user, movie=self.movie, tag="Delete Tag")
        url = detail_url(tag.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tags.objects.filter(id=tag.id).exists())

    def test_unauthorized_tag_update(self):
        """
        Test that a tag cannot be updated by another user.
        """

        new_user = get_user_model().objects.create_user(
            email="newuser@example.com", password="newpass123"
        )
        tag = create_tag(user=new_user, movie=self.movie, tag="Original Tag")
        payload = {"tag": "Unauthorized Update"}

        url = detail_url(tag.id)
        res = self.client.patch(url, payload)
        tag.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(tag.tag, "Original Tag")

    def test_unauthorized_tag_delete(self):
        """
        Test that a tag cannot be deleted by another user.
        """
        new_user = get_user_model().objects.create_user(
            email="newuser@example.com", password="newpass123"
        )
        tag = create_tag(user=new_user, movie=self.movie, tag="Delete Tag")

        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Tags.objects.filter(id=tag.id).exists())
