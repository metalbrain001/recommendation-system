"""
This Module streams the ratings
data directly into the PostgreSQL
database using the COPY command.
"""

import csv
import io
from datetime import datetime
from django.db import connection
from django.contrib.auth import get_user_model


class StreamRatingToDb:
    def __init__(self, path=""):
        self.path = path

    def create_user(self, user_id):
        """
        Create a new user in the database.
        """

        User = get_user_model()
        email = f"user_{user_id}@example.com"
        user = User.objects.create_user(
            id=user_id,
            email=email,
        )
        return user

    def check_rating_exists(self, user_id, movie_id):
        """
        Check if a rating already exists
        in the database.
        """

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id
                FROM core_ratings
                WHERE user_id = %s
                AND movie_id = %s
                """,
                [user_id, movie_id]
            )
            return cursor.fetchone()

    def stream_ratings_to_db(self, chunk_size=10000):
        """
        Stream ratings data directly
        into the PostgreSQL database
        with on-the-fly timestamp
        conversion using the COPY command.
        """

        file_path = f"{self.path}/ratings.csv"

        try:
            with connection.cursor() as cursor:
                with open(file_path, 'r') as f:
                    reader = csv.reader(f)
                    header = next(reader)
                    header = [col.strip() for col in header]

                    # Process the data in chunks
                    while True:
                        chunk = [row for _, row in zip(range(chunk_size),
                                                       reader)]
                        if not chunk:
                            break

                        # Convert timestamps and write to in-memory file
                        csv_buffer = io.StringIO()
                        writer = csv.writer(csv_buffer)

                        # Write header
                        writer.writerow(
                          ['user_id',
                           'movie_id',
                           'rating',
                           'timestamp',
                           'created_at'])

                        for row in chunk:
                            user_id = int(row[0])
                            self.create_user(user_id)
                            row[3] = datetime.utcfromtimestamp(
                              int(row[3])).strftime('%Y-%m-%d %H:%M:%S')
                            created_at = datetime.now().strftime(
                              '%Y-%m-%d %H:%M:%S')
                            row.append(created_at)

                            writer.writerow(row)

                        # Move to the beginning of the in-memory file
                        csv_buffer.seek(0)

                        # Stream the modified chunk to the database
                        cursor.copy_expert(
                            """
                            COPY core_ratings
                            (user_id, movie_id, rating, timestamp, created_at)
                            FROM STDIN WITH CSV HEADER
                            """,
                            csv_buffer
                        )

                        print(f"Inserted {len(chunk)} rows...")

            print("Ratings streamed successfully!")

        except Exception as e:
            print(f"An error occurred: {e}")
