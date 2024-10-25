"""
This Module contains the MovieLens data loading functions.
"""

import pandas as pd


class MovieLensDataLoader:
    """
    Class to load the MovieLens data.
    """

    def __init__(self, data_path=""):
        """
        Constructor for the MovieLensDataLoader class.

        :param data_path: The path to the MovieLens data.
        """
        self.data_path = data_path

    def load_data(self):
        """
        Load the MovieLens data files.
        (Movies, Ratings, Tags, Links)

        :return: The MovieLens data as a pandas DataFrame.
        """

        try:
            MOVIES = pd.read_csv(f"{self.data_path}movies.csv")
            RATINGS = pd.read_csv(f"{self.data_path}ratings.csv")
            TAGS = pd.read_csv(f"{self.data_path}tags.csv")
            LINKS = pd.read_csv(f"{self.data_path}links.csv")
            print("Data loaded successfully!")
            return MOVIES, RATINGS, TAGS, LINKS
        except FileNotFoundError as e:
            print(f"Error loading data: {e}")
            return None, None, None, None
