import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from src.recommender.utils import download_movielens_dataset


def load_data(data_path='data/ml-latest-small'):
    """
    Load MovieLens dataset and return processed DataFrames.
    If data doesn't exist, attempt to download it.
    """
    # Check if data directory exists
    if not os.path.exists(data_path):
        print(f"Data directory {data_path} not found. Attempting to download dataset...")
        if not download_movielens_dataset():
            raise FileNotFoundError(f"Could not download or find the dataset at {data_path}")
    
    ratings_path = os.path.join(data_path, 'ratings.csv')
    movies_path = os.path.join(data_path, 'movies.csv')
    
    # Verify files exist
    if not os.path.exists(ratings_path) or not os.path.exists(movies_path):
        print("Data files not found. Attempting to download dataset...")
        if not download_movielens_dataset():
            raise FileNotFoundError(f"Could not download or find the dataset files in {data_path}")
    
    # Load ratings and movies data
    ratings = pd.read_csv(ratings_path)
    movies = pd.read_csv(movies_path)
    
    print(f"Loaded {len(ratings)} ratings from {ratings['userId'].nunique()} users on {ratings['movieId'].nunique()} movies")
    
    return ratings, movies

def prepare_data(ratings, test_size=0.2, random_state=42):
    """
    Split data into train and test sets.
    """
    # First, group by user to ensure each user has both train and test data
    user_groups = {}
    for user_id, group in ratings.groupby('userId'):
        # For each user, split their ratings
        if len(group) >= 5:  # Only consider users with enough ratings
            train, test = train_test_split(
                group, 
                test_size=min(test_size, 0.5),  # Ensure we don't take too many for test
                random_state=random_state
            )
            user_groups[user_id] = (train, test)
    
    # Combine all users' train and test data
    train_data = pd.concat([t[0] for t in user_groups.values()])
    test_data = pd.concat([t[1] for t in user_groups.values()])
    
    print(f"Split data into {len(train_data)} training and {len(test_data)} testing samples")
    
    # Create user-item matrix from training data
    user_item_matrix = train_data.pivot(
        index='userId', 
        columns='movieId', 
        values='rating'
    ).fillna(0)
    
    return user_item_matrix, train_data, test_data

def get_movie_features(movies):
    """
    Extract features from movie metadata (genres).
    """
    # One-hot encode genres
    genres = movies['genres'].str.get_dummies('|')
    
    # Combine with movie IDs
    movie_features = pd.concat([movies[['movieId']], genres], axis=1)
    
    return movie_features
