import csv
import io
from datetime import datetime, timezone
from django.db import connection
from django.contrib.auth import get_user_model


class StreamTagToDb:
    def __init__(self, path=""):
        self.path = path

    def create_user(self, user_id):
        """
        Create a new user in the database.
        """
        User = get_user_model()
        email = f"user_{user_id}@example.com"
        user, created = User.objects.get_or_create(
            id=user_id,
            email=email,
        )
        return user

    def check_tag_exists(self, user_id, movie_id):
        """
        Check if a tag already exists in the database.
        """

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id
                FROM core_tags
                WHERE user_id = %s
                AND movie_id = %s
                """,
                [user_id, movie_id]
            )
            return cursor.fetchone()

    def convert_unix_timestamp(self, unix_timestamp):
        """
        Convert Unix timestamp to Python datetime object.
        """
        return datetime.fromtimestamp(int(unix_timestamp), timezone.utc)

    def stream_tags_to_db(self, chunk_size=10000):
        """
        Stream tags data directly into the PostgreSQL database
        with on-the-fly timestamp conversion using the COPY command.
        """
        file_path = f"{self.path}/tags.csv"

        try:
            with connection.cursor() as cursor:
                with open(file_path, 'r') as f:
                    reader = csv.reader(f, quotechar='"', delimiter=',')
                    next(reader)
                    buffer = io.StringIO()
                    writer = csv.writer(buffer)

                    for i, row in enumerate(reader):
                        user_id = int(row[0])
                        movie_id = int(row[1])
                        tag = row[2]
                        unix_timestamp = int(row[3])

                        tag_exists = self.check_tag_exists(user_id, movie_id)

                        if tag_exists:
                            print(
                                f"Tag already exist for:"
                                f"{user_id}, movie_id: {movie_id}"
                            )
                            continue

                        # Create user if not already exists
                        user = self.create_user(user_id)

                        # Convert timestamp
                        timestamp = self.convert_unix_timestamp(unix_timestamp)

                        # Write to buffer in proper format
                        writer.writerow([user.id, movie_id, tag, timestamp])

                    # Use an INSERT statement instead of COPY
                    cursor.execute(
                        """
                        INSERT INTO core_tags (user_id,
                        movie_id, tag, timestamp)
                        VALUES (%s, %s, %s, %s)
                        """,
                        [user.id, movie_id, tag, timestamp]
                    )

                print("Tags data streamed successfully!")

        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None
