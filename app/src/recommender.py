import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import matplotlib.pyplot as plt
from surprise import accuracy
import pickle

plt.style.use("dark_background")


class RecommenderSystem:
    """
    Class for content and collaborative
    filtering recommendations using CSV snapshots.
    """

    def __init__(self, data_path="", model_path=""):
        # Initialize with path to CSV snapshots
        self.data_path = data_path
        self.model_path = model_path
        self.movies = self.load_movies()
        self.ratings = self.load_ratings()
        self.svd_model = None
        os.makedirs(self.model_path, exist_ok=True)

    def load_movies(self):
        """
        Load movie data from the snapshot CSV file.
        """

        try:
            movies_df = pd.read_csv(f"{self.data_path}/movies.csv")
            return movies_df
        except FileNotFoundError as e:
            print(f"Error loading movies data: {e}")
            return pd.DataFrame()

    def load_ratings(self):
        """
        Load ratings data from the snapshot CSV file.
        """

        try:
            ratings_df = pd.read_csv(f"{self.data_path}/ratings.csv")
            return ratings_df
        except FileNotFoundError as e:
            print(f"Error loading ratings data: {e}")
            return pd.DataFrame()

    def content_based_filtering(self, movie_title, top_n=10):
        """
        Content-based filtering recommendation
        based on movie genres.
        """

        # Validate genres column
        if self.movies["genres"].isnull().all():
            raise ValueError("Genres column contains only null values.")
        if self.movies["genres"].str.strip().eq("").all():
            raise ValueError("Genres column contains no valid data.")

        # Validate input movie title
        matched_movies = self.movies[
            self.movies["title"].str.contains(movie_title, na=False, case=False)
        ]
        if matched_movies.empty or len(matched_movies) > 1:
            raise ValueError(
                f"Movie title '{movie_title}' not uniquely matched or not found."
            )
        idx = matched_movies.index[0]

        # Create TF-IDF matrix
        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf.fit_transform(self.movies["genres"].fillna(""))
        if tfidf_matrix.shape[0] == 0:
            raise ValueError("TF-IDF matrix is empty; cannot compute recommendations.")

        # Compute cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Get similarity scores for all movies
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get top-n recommendations
        movie_indices = [i[0] for i in sim_scores[1 : top_n + 1]]  # noqa: E203
        return self.movies["title"].iloc[movie_indices]

    def collaborative_filtering(self):
        """
        Train a collaborative filtering model
        using SVD from the Surprise library.
        """

        if self.ratings.empty:
            raise ValueError("No ratings data found in the dataset.")

        # Load data into Surprise Dataset
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(
            self.ratings[["user_id", "movie_id", "rating"]], reader
        )

        # Split data into training and testing sets
        trainset, testset = train_test_split(data, test_size=0.25)
        self.svd_model = SVD()
        self.svd_model.fit(trainset)

        # Test the model
        self.predictions = self.svd_model.test(testset)
        return self.svd_model, self.predictions

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

    def evaluate_content_filtering(self, sample_movies, top_n=10):
        results = {}
        for movie in sample_movies:
            recommendations = self.content_based_filtering(movie, top_n=top_n)
            results[movie] = recommendations
        return results

    def evaluate_collaborative_filtering(self, sample_users, top_n=10):
        results = {}
        for user in sample_users:
            recommendations = self.recommend_movies(user, self.svd_model, top_n=top_n)
            results[user] = recommendations
        return results

    # RMSE and MAE calculation
    def calculate_metrics(self):
        rmse = accuracy.rmse(self.predictions, verbose=False)
        mae = accuracy.mae(self.predictions, verbose=False)
        return rmse, mae

    def get_user_feedback(self, recommendations):
        feedback = {}
        for movie in recommendations:
            rating = input(f"Rate the recommendation for '{movie}' (1-5): ")
            feedback[movie] = int(rating)
        return feedback

    def save_models(self):
        """
        Save the trained models to disk.
        """

        content_model_path = os.path.join(self.model_path, "content_based_model.pkl")

        collaborative_model_path = os.path.join(
            self.model_path, "collaborative_model.pkl"
        )

        # Save content-based filtering model (e.g., TF-IDF matrix or similar)
        with open(content_model_path, "wb") as f:
            pickle.dump(self, f)

        # Save collaborative filtering model
        with open(collaborative_model_path, "wb") as f:
            pickle.dump(self.svd_model, f)

        print(f"Models saved at {self.model_path}")

    def load_models(self):
        """
        Load the trained models from disk.
        """
        # Paths for loading models
        content_model_path = os.path.join(self.model_path, "content_based_model.pkl")
        collaborative_model_path = os.path.join(
            self.model_path, "collaborative_model.pkl"
        )

        # Load content-based model
        with open(content_model_path, "rb") as f:
            content_based_model = pickle.load(f)

        # Load collaborative filtering model
        with open(collaborative_model_path, "rb") as f:
            self.svd_model = pickle.load(f)

        print("Models loaded successfully.")
        return content_based_model, self.svd_model
