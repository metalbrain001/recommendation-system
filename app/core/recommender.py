import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from core.models import Movie, Ratings
from django_pandas.io import read_frame


class RecommenderSystem:
    """
    Class for content and collaborative
    filtering recommendations using Django ORM.
    """

    def __init__(self):
        # Load data from the database
        self.movies = self.load_movies()
        self.ratings = self.load_ratings()

    def load_movies(self):
        """
        Load movie data from the
        Django Movie model into a DataFrame.
        """

        queryset = Movie.objects.all()
        return read_frame(queryset, fieldnames=["movie_id", "title", "genres"])

    def load_ratings(self):
        """
        Load ratings data from the
        Django Ratings model into a DataFrame.
        """

        queryset = Ratings.objects.all()
        return read_frame(queryset, fieldnames=["user_id", "movie_id", "rating"])

    def content_based_filtering(self, movie_title, top_n=10):
        """
        Content-based filtering recommendation based on movie genres.
        Recommends movies similar to the given movie title.
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
        movie_indices = [i[0] for i in sim_scores[1 : top_n + 1]]
        return self.movies["title"].iloc[movie_indices]

    def collaborative_filtering(self):
        """
        Train a collaborative filtering
        model using SVD from the Surprise library.
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
        user using the collaborative filtering model.
        """

        all_movie_ids = self.ratings["movie_id"].unique()
        all_movie_ids = [
            int(movie_id)
            for movie_id in all_movie_ids
            if isinstance(movie_id, (int, np.integer))
        ]

        rated_movie_ids = self.ratings[self.ratings["user_id"] == user_id]["movie_id"]
        movies_not_rated = set(all_movie_ids) - set(rated_movie_ids)

        predictions = [
            (movie_id, svd_model.predict(user_id, movie_id).est)
            for movie_id in movies_not_rated
        ]

        # Sort movies by predicted rating and select the top recommendations
        predictions.sort(key=lambda x: x[1], reverse=True)
        recommended_movie_ids = [movie_id for movie_id, _ in predictions[:top_n]]

        recommended_movies = Movie.objects.filter(movie_id__in=recommended_movie_ids)
        return [movie.title for movie in recommended_movies]
