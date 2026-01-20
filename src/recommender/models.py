import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

class CollaborativeFiltering:
    """
    Collaborative filtering recommendation model.
    """
    
    def __init__(self, k=10):
        """Initialize with number of neighbors k."""
        # Ensure k is an integer to prevent sklearn errors
        self.k = int(k)
        self.model = None
        self.user_item_matrix = None
    
    def fit(self, user_item_matrix):
        """
        Train the model using user-item matrix.
        """
        self.user_item_matrix = user_item_matrix
        
        # Create sparse matrix for efficiency
        user_item_sparse = csr_matrix(user_item_matrix.values)
        
        # Train KNN model
        self.model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=self.k+1)
        self.model.fit(user_item_sparse)
        
        return self
    
    def recommend_items(self, user_id, n_recommendations=5):
        """
        Recommend top N items for a user.
        """
        if user_id not in self.user_item_matrix.index:
            print(f"User {user_id} not found in training data")
            return pd.DataFrame()
        
        # Get user's item ratings vector
        user_vector = self.user_item_matrix.loc[user_id].values.reshape(1, -1)
        user_vector_sparse = csr_matrix(user_vector)
        
        try:
            # Find similar users
            distances, indices = self.model.kneighbors(user_vector_sparse, n_neighbors=min(self.k+1, len(self.user_item_matrix)))
            
            # Get indices of similar users (exclude the user itself)
            similar_users = [self.user_item_matrix.index[idx] for idx in indices.flatten()[1:]]
            
            # Build recommendations based on what similar users liked
            user_rated_items = set(self.user_item_matrix.columns[self.user_item_matrix.loc[user_id] > 0])
            recommendations = {}
            
            # Calculate weighted ratings from similar users
            for similar_user in similar_users:
                similar_user_ratings = self.user_item_matrix.loc[similar_user]
                
                # Consider items that the target user hasn't rated
                for item in self.user_item_matrix.columns:
                    item_id = item  # The column name is the item ID
                    if similar_user_ratings[item] > 0 and item not in user_rated_items:
                        if item_id not in recommendations:
                            recommendations[item_id] = 0
                        # The closer the similar user, the more weight their recommendation has
                        recommendations[item_id] += similar_user_ratings[item]
            
            # If no recommendations found, try using average ratings
            if not recommendations:
                # Find items the user hasn't rated but are generally well-rated
                item_means = self.user_item_matrix.mean().sort_values(ascending=False)
                for item, rating in item_means.items():
                    if item not in user_rated_items and rating > 0:
                        recommendations[item] = rating
                        if len(recommendations) >= n_recommendations:
                            break
            
            # Sort by recommendation strength
            sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
            
            # Return top N recommendations
            top_recommendations = pd.DataFrame(sorted_recommendations[:n_recommendations], 
                                              columns=['movieId', 'score'])
            
            return top_recommendations
            
        except Exception as e:
            print(f"Error generating recommendations for user {user_id}: {e}")
            return pd.DataFrame()

class ContentBasedFiltering:
    """
    Content-based recommendation model.
    """
    
    def __init__(self):
        """Initialize the content-based model."""
        self.movie_features = None
        self.similarity_matrix = None
        self.movies_df = None
    
    def fit(self, movie_features, movies_df):
        """
        Train the model using movie features.
        """
        self.movie_features = movie_features
        self.movies_df = movies_df
        
        # Extract feature matrix without movie IDs
        feature_matrix = movie_features.drop('movieId', axis=1).values
        
        # Calculate similarity matrix
        self.similarity_matrix = cosine_similarity(feature_matrix)
        
        return self
    
    def recommend_similar_movies(self, movie_id, n_recommendations=5):
        """
        Recommend similar movies based on a given movie ID.
        """
        # Find the index of the movie in the feature matrix
        movie_indices = self.movie_features.index[self.movie_features['movieId'] == movie_id].tolist()
        
        if not movie_indices:
            return pd.DataFrame()
        
        movie_idx = movie_indices[0]
        
        # Get similarity scores for this movie with all others
        similarity_scores = list(enumerate(self.similarity_matrix[movie_idx]))
        
        # Sort movies by similarity score
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        
        # Get the top N most similar movies (excluding itself)
        similar_movies_indices = [i[0] for i in similarity_scores[1:n_recommendations+1]]
        
        # Get the movie IDs
        similar_movie_ids = self.movie_features.iloc[similar_movies_indices]['movieId'].values
        similarity_values = [i[1] for i in similarity_scores[1:n_recommendations+1]]
        
        # Create recommendations dataframe
        recommendations = pd.DataFrame({
            'movieId': similar_movie_ids,
            'similarity': similarity_values
        })
        
        return recommendations

class HybridRecommender:
    """
    Hybrid recommendation model that combines collaborative and content-based filtering.
    """
    
    def __init__(self, cf_weight=0.7):
        """Initialize with weight for collaborative filtering recommendations."""
        self.cf_model = CollaborativeFiltering(k=20)
        self.cb_model = ContentBasedFiltering()
        self.cf_weight = cf_weight
        self.item_popularity = None
        self.movies_df = None
        
    def fit(self, user_item_matrix, movie_features, movies_df, ratings_df):
        """Train both models and compute item popularity."""
        # Train component models
        self.cf_model.fit(user_item_matrix)
        self.cb_model.fit(movie_features, movies_df)
        self.movies_df = movies_df
        
        # Calculate item popularity
        self.item_popularity = ratings_df.groupby('movieId')['rating'].agg(['count', 'mean'])
        self.item_popularity['score'] = self.item_popularity['count'] * self.item_popularity['mean']
        self.item_popularity = self.item_popularity.sort_values('score', ascending=False)
        
        return self
        
    def recommend_items(self, user_id, n_recommendations=5):
        """Get hybrid recommendations for a user."""
        # Get collaborative filtering recommendations
        cf_recs = self.cf_model.recommend_items(user_id, n_recommendations=n_recommendations*2)
        
        if cf_recs.empty:
            # Fallback to popularity-based recommendations
            popular_items = self.item_popularity.index[:n_recommendations].tolist()
            return pd.DataFrame({'movieId': popular_items, 'score': range(n_recommendations, 0, -1)})
        
        # Get user's top-rated movie
        user_vector = self.cf_model.user_item_matrix.loc[user_id]
        if user_vector.max() > 0:
            top_movie_id = user_vector.idxmax()
            # Get content-based recommendations
            cb_recs = self.cb_model.recommend_similar_movies(top_movie_id, n_recommendations=n_recommendations*2)
        else:
            cb_recs = pd.DataFrame()
            
        # If no content-based recommendations, just return collaborative filtering
        if cb_recs.empty:
            return cf_recs.head(n_recommendations)
            
        # Merge and weight the recommendations
        # Normalize scores for both recommendation types
        cf_recs['normalized_score'] = cf_recs['score'] / cf_recs['score'].max()
        cb_recs['normalized_score'] = cb_recs['similarity'] / cb_recs['similarity'].max()
        
        # Combine recommendations
        cf_recs = cf_recs.rename(columns={'normalized_score': 'cf_score'})
        cb_recs = cb_recs.rename(columns={'normalized_score': 'cb_score'})
        
        # Outer join to get all recommendations
        hybrid_recs = pd.merge(cf_recs[['movieId', 'cf_score']], 
                              cb_recs[['movieId', 'cb_score']], 
                              on='movieId', 
                              how='outer').fillna(0)
        
        # Calculate weighted hybrid score
        hybrid_recs['score'] = (self.cf_weight * hybrid_recs['cf_score'] + 
                               (1 - self.cf_weight) * hybrid_recs['cb_score'])
        
        # Sort and take top N
        return hybrid_recs.sort_values('score', ascending=False)[['movieId', 'score']].head(n_recommendations)
