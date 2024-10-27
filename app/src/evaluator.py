"""
Module for evaluating collaborative filtering model.
"""

from surprise import accuracy
import numpy as np


class Evaluator:
    """
    Class to evaluate collaborative filtering model.
    """

    def __init__(self):
        pass

    def evaluate_rmse(self, predictions):
        """
        Evaluate RMSE (Root Mean Squared Error)
        for collaborative filtering model.
        """

        return accuracy.rmse(predictions)

    def evaluate_precision_at_k(self, predictions, k=10):
        """
        Evaluate Precision@K for top-n recommendations.
        """

        user_est_true = {}
        for uid, _, true_r, est, _ in predictions:
            if uid not in user_est_true:
                user_est_true[uid] = []
            user_est_true[uid].append((est, true_r))
        precisions = []
        for uid, user_ratings in user_est_true.items():
            # Sort by estimated rating
            user_ratings.sort(key=lambda x: x[0], reverse=True)
            # Number of relevant items
            relevant = sum((true_r >= 4.0) for (_, true_r) in user_ratings[:k])
            # Precision@K
            precisions.append(relevant / k)
        return np.mean(precisions)
