import csv
import io
from django.db import connection


class StreamLinksToDb:
    def __init__(self, path=""):
        self.path = path

    def stream_links_to_db(self):
        """
        Stream links data directly into
        the PostgreSQL database
        using the COPY command.
        """
        file_path = f"{self.path}/links.csv"

        try:
            with connection.cursor() as cursor:
                with open(file_path, 'r') as f:
                    reader = csv.reader(f)
                    next(reader)
                    buffer = io.StringIO()
                    writer = csv.writer(buffer)

                    for row in reader:
                        movie_id = int(row[0])
                        imdb_id = int(row[1])
                        tmdb_id = float(row[2])

                        # Write to buffer in proper format
                        writer.writerow([movie_id, imdb_id, tmdb_id])

                    buffer.seek(0)
                    cursor.copy_from(
                        buffer, 'core_links',
                        columns=('movie_id', 'imdb_id', 'tmdb_id'),
                        sep=','
                    )
                    buffer.truncate(0)

                print("Links data streamed successfully!")

        except FileNotFoundError as e:
            print(f"Error: {e}")
