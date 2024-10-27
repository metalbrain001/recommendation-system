"""
This module contains the test for link API
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from core.models import Links, Movie
from links.serializer import LinkDetailSerializer


LINKS_URL = reverse("links:link-list")


def detail_url(link_id):
    """
    Return link detail URL.
    """

    return reverse("links:link-detail", args=[link_id])


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


def create_links(movie, imdb_id=114709, tmdb_id=862):
    """
    Helper function to create
    a link for a movie.
    """

    return Links.objects.create(movie=movie, imdb_id=imdb_id, tmdb_id=tmdb_id)


class PublicLinkApiTests(TestCase):
    """
    Test the publicly available links API.
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that authentication is required for retrieving links.
        """

        res = self.client.get(LINKS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateLinkApiTests(TestCase):
    """
    Test the private links API.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "links@example.com", "testpass123"
        )
        self.client.force_authenticate(self.user)
        self.movie = create_movie(user=self.user)

    def test_list_links(self):
        """
        Test retrieving a list of links.
        """

        create_links(movie=self.movie)
        create_links(movie=self.movie)
        res = self.client.get(LINKS_URL)
        links = Links.objects.all().order_by("-id")
        serializer = LinkDetailSerializer(links, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_links_limited_to_user(self):
        """
        Test that links returned
        are for the authenticated user.
        """

        user2 = get_user_model().objects.create_user(
            "testuser@example.com", "testpass123"
        )

        movie2 = create_movie(user=user2, movie_id=405)
        create_links(movie=movie2)
        link = create_links(movie=self.movie)
        res = self.client.get(LINKS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["results"][0]["imdb_id"], link.imdb_id)
        self.assertEqual(res.data["results"][0]["tmdb_id"], link.tmdb_id)

    def test_create_link_successful(self):
        """
        Test creating a new link.
        """

        payload = {
            "movie": self.movie.movie_id,
            "imdb_id": 114709,
            "tmdb_id": 862,
        }

        res = self.client.post(LINKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        link = Links.objects.get(movie=self.movie)
        self.assertEqual(link.movie.movie_id, self.movie.movie_id)
        self.assertEqual(link.imdb_id, payload["imdb_id"])
        self.assertEqual(link.tmdb_id, payload["tmdb_id"])
        self.assertEqual(res.data["movie"], self.movie.movie_id)

    def test_create_link_invalid(self):
        """
        Test creating a new link with invalid payload.
        """

        payload = {
            "movie": "",
            "imdb_id": 114709,
            "tmdb_id": 862,
        }

        res = self.client.post(LINKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["movie"], ["This field may not be null."])

    def test_update_link(self):
        """
        Test updating a link.
        """

        link = create_links(movie=self.movie)
        payload = {
            "imdb_id": 114709,
            "tmdb_id": 862,
        }

        url = detail_url(link.id)
        res = self.client.patch(url, payload)
        link.refresh_from_db()
        self.assertEqual(link.imdb_id, payload["imdb_id"])
        self.assertEqual(link.tmdb_id, payload["tmdb_id"])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_link(self):
        """
        Test deleting a link.
        """

        link = create_links(movie=self.movie)
        url = detail_url(link.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Links.objects.count(), 0)

    def test_retrieve_link(self):
        """
        Test retrieving a link.
        """

        link = create_links(movie=self.movie)
        url = detail_url(link.id)
        res = self.client.get(url)
        serializer = LinkDetailSerializer(link)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unauthorized_delete_link(self):
        """
        Test deleting a link without permission.
        """

        user2 = get_user_model().objects.create_user(
            "notuser@example.com", "testpass123"
        )

        movie2 = create_movie(user=user2, movie_id=405)
        link = create_links(movie=movie2)
        url = detail_url(link.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Links.objects.count(), 1)
