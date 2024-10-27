import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split


class RecommenderSystem:
    """
    Class for content and collaborative
    filtering recommendations using direct
    PostgreSQL querying.
    """

    def __init__(self):
        # Establish a connection to PostgreSQL using SQLAlchemy
        db_uri = "postgresql://timeless:password@localhost:5432/devdb"
        self.engine = create_engine(db_uri)
        self.movies = self.load_movies()
        self.ratings = self.load_ratings()

    def load_movies(self):
        """
        Directly load movie data from
        PostgreSQL into a DataFrame.
        """

        query = "SELECT movie_id, title, genres FROM core_movie;"
        movies_df = pd.read_sql_query(query, self.engine)
        return movies_df

    def load_ratings(self):
        """
        Directly load ratings data from
        PostgreSQL into a DataFrame.
        """

        query = "SELECT user_id, movie_id, rating FROM core_ratings;"
        ratings_df = pd.read_sql_query(query, self.engine)
        return ratings_df

    def content_based_filtering(self, movie_title, top_n=10):
        """
        Content-based filtering recommendation
        based on movie genres.
        """

        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf.fit_transform(self.movies["genres"])

        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Find the index of the movie that matches the title
        try:
            idx = self.movies[self.movies["title"] == movie_title].index[0]
        except IndexError:
            return f"Movie titled '{movie_title}' not found in the database."

        # Get similarity scores for all movies
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the top-n movie indices based on similarity
        movie_indices = [i[0] for i in sim_scores[1 : top_n + 1]]  # noqa: E203
        return self.movies["title"].iloc[movie_indices]

    def collaborative_filtering(self):
        """
        Train a collaborative filtering model
        using SVD from the Surprise library.
        """

        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(
            self.ratings[["user_id", "movie_id", "rating"]], reader
        )

        # Split data into training and testing sets
        trainset, testset = train_test_split(data, test_size=0.25)
        svd = SVD()
        svd.fit(trainset)

        # Test the model
        predictions = svd.test(testset)
        return svd, predictions

    def recommend_movies(self, user_id, svd_model, top_n=10):
        """
        Recommend top-n movies for a given
        user using collaborative filtering.
        """

        all_movie_ids = self.ratings["movie_id"].unique()
        rated_movie_ids = self.ratings[self.ratings["user_id"] == user_id]["movie_id"]
        movies_not_rated = set(all_movie_ids) - set(rated_movie_ids)

        predictions = [
            (movie_id, svd_model.predict(user_id, movie_id).est)
            for movie_id in movies_not_rated
        ]

        # Sort movies by predicted rating and select the top recommendations
        predictions.sort(key=lambda x: x[1], reverse=True)
        recommended_movie_ids = [movie_id for movie_id, _ in predictions[:top_n]]

        recommended_movies = self.movies[
            self.movies["movie_id"].isin(recommended_movie_ids)
        ]
        return recommended_movies["title"].tolist()
