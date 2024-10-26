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
