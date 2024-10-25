from django.test import TestCase
from core.models import Tags, Movie
from django.contrib.auth import get_user_model


class TagModelTest(TestCase):
    """
    Test bulk insertion of tags.
    """

    def test_tag_bulk_insert(self):
        """
        Test bulk insert of tags into the Tag model.
        """

        # Create dummy users using the get_user_model()
        user1 = get_user_model().objects.create_user(
             email="user1@example.com", password="testpass123"
        )
        user2 = get_user_model().objects.create_user(
             email="user2@example.com", password="testpass123"
        )

        # Create dummy movies for ForeignKey relationships
        movie1 = Movie.objects.create(
            movie_id=1,
            title="God Father",
            genres="Action",
            user=user1
            )
        movie2 = Movie.objects.create(
            movie_id=2,
            title="The Matrix",
            genres="Action",
            user=user2
            )

        # Define the tag data to be inserted, using the correct fields
        tag_data = [
            Tags(
                user=user1, movie=movie1, tag="Kevin Kline",
            ),
            Tags(
                user=user1, movie=movie2, tag="misogyny",
            ),
            Tags(
                user=user2, movie=movie2, tag="action",
            ),
        ]

        # Perform bulk insert of tags
        Tags.objects.bulk_create(tag_data)

        # Assert that 3 tags were inserted
        self.assertEqual(Tags.objects.count(), 3)

        # Fetch the tags in a deterministic order (order by id)
        tags = Tags.objects.order_by('id')

        # Create expected data, using user and movie IDs for comparison
        inserted_data = [
            (
              user1.id, movie1.movie_id, "Kevin Kline",),
            (
              user1.id, movie2.movie_id, "misogyny",),
            (
              user2.id, movie2.movie_id, "action",),
        ]

        # Compare fetched tags with expected data
        for i, tag in enumerate(tags):
            self.assertEqual(tag.user.id, inserted_data[i][0])
            self.assertEqual(tag.movie.movie_id, inserted_data[i][1])
            self.assertEqual(tag.tag, inserted_data[i][2])
