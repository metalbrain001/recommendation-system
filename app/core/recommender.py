import os
import pandas as pd
from surprise.model_selection import train_test_split
from sqlalchemy import create_engine
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD
from sklearn.metrics.pairwise import linear_kernel


class RecommenderSystem:
    def __init__(self):
        # Establish a connection to PostgreSQL using SQLAlchemy
        db_uri = "postgresql://timeless:password@localhost:5432/devdb"
        self.engine = create_engine(db_uri)
        self._movies = None
        self._ratings = None

    @property
    def movies(self):
        if self._movies is None:
            self._movies = self.load_movies()
        return self._movies

    @property
    def ratings(self):
        if self._ratings is None:
            self._ratings = self.load_ratings()
        return self._ratings

    def load_movies(self):
        query = "SELECT movie_id, title, genres FROM core_movie;"
        return pd.read_sql_query(query, self.engine)

    def load_ratings(self):
        query = "SELECT user_id, movie_id, rating FROM core_ratings;"
        return pd.read_sql_query(query, self.engine)

    def save_model(self, model, filename):
        with open(filename, "wb") as f:
            pickle.dump(model, f)

    def load_model(self, filename):
        with open(filename, "rb") as f:
            return pickle.load(f)

    def content_based_filtering(self, movie_title, top_n=10):
        """
        Content-based filtering recommendation based on movie genres.
        """

        # Preprocess genres
        if "genres" not in self.movies or self.movies["genres"].isnull().all():
            return "No genres found in the dataset."
        self.movies["genres"] = self.movies["genres"].fillna("").str.replace("|", " ")

        # Create the TF-IDF matrix
        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf.fit_transform(self.movies["genres"])

        if tfidf_matrix.shape[0] == 0:
            raise ValueError("TF-IDF matrix is empty. Check your genres data.")

        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        try:
            # Match movie title
            matched_movies = self.movies[self.movies["title"] == movie_title]

            if matched_movies.empty:
                raise ValueError(
                    f"Movie titled '{movie_title}' not found in the database."
                )

            if len(matched_movies) > 1:
                print(
                    f"Multiple matches found for '{movie_title}', using the first match."
                )

            idx = matched_movies.index[0]

        except IndexError:
            return f"Movie titled '{movie_title}' not found in the database."

        # Calculate similarity scores
        try:
            sim_scores = list(enumerate(cosine_sim[idx]))
        except IndexError as e:
            return f"Error calculating similarity scores for movie index {idx}."

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Retrieve top-n movie recommendations
        try:
            movie_indices = [i[0] for i in sim_scores[1 : top_n + 1]]
            recommendations = self.movies["title"].iloc[movie_indices]
            return recommendations.tolist()

        except Exception as e:
            return f"Error generating recommendations: {str(e)}"

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

    def train_and_save_content_based_model(self, filename="content_model.pkl"):
        """
        Train a content-based filtering
        model and save it to a file.
        """
        # Ensure 'genres' is processed as text
        # self.movies["genres"] = self.movies["genres"].fillna("")
        movies_sampled = self.movies.sample(n=5000, random_state=42).fillna("")

        # Create the TF-IDF matrix based on the 'genres' column
        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf.fit_transform(movies_sampled["genres"])

        # Compute cosine similarity between all movies
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        # Save the model (e.g., as a dictionary with titles and similarity matrix)
        content_based_model = {
            "cosine_sim": cosine_sim,
            "title": self.movies["title"],
        }
        self.save_model(content_based_model, filename)
        print(f"Content-based model saved to {filename}")

    def train_and_save_collaborative_model(self, filename="collaborative_model.pkl"):
        svd, predictions = self.collaborative_filtering()
        self.save_model(svd, filename)
        print(f"Collaborative model saved to {filename}")
        return svd

    def load_content_based_model(self, filename="content_model.pkl"):
        return self.load_model(filename)

    def load_collaborative_model(self, filename="collaborative_model.pkl"):
        return self.load_model(filename)
