import pandas as pd
import numpy as np
from src.recommender.models import CollaborativeFiltering, HybridRecommender
from src.recommender.evaluation import evaluate_recommendations

def tune_collaborative_filtering(user_item_matrix, train_data, test_data, movies):
    """Find optimal number of neighbors for collaborative filtering"""
    print("Tuning collaborative filtering parameters...")
    k_values = [5, 10, 15, 20, 30, 50]
    results = []
    
    for k in k_values:
        print(f"Testing with k={k}...")
        # Ensure k is an integer
        model = CollaborativeFiltering(k=int(k))
        model.fit(user_item_matrix)
        
        precision, recall, hit_rate = evaluate_recommendations(
            model, test_data, movies, k=10, verbose=False
        )
        
        results.append({
            'k': k,
            'precision': precision,
            'recall': recall,
            'hit_rate': hit_rate
        })
    
    results_df = pd.DataFrame(results)
    print("\nCollaborative filtering tuning results:")
    print(results_df)
    
    best_k = results_df.loc[results_df['hit_rate'].idxmax()]['k']
    print(f"Best k value: {best_k}")
    
    # Return as an integer to avoid issues
    return int(best_k)

def tune_hybrid_weights(user_item_matrix, movie_features, train_data, test_data, movies):
    """Find optimal weighting between collaborative and content-based"""
    print("Tuning hybrid recommender weights...")
    weights = [0.3, 0.5, 0.7, 0.9]
    results = []
    
    for weight in weights:
        print(f"Testing with cf_weight={weight}...")
        model = HybridRecommender(cf_weight=weight)
        model.fit(user_item_matrix, movie_features, movies, train_data)
        
        precision, recall, hit_rate = evaluate_recommendations(
            model, test_data, movies, k=10, verbose=False
        )
        
        results.append({
            'cf_weight': weight,
            'precision': precision,
            'recall': recall,
            'hit_rate': hit_rate
        })
    
    results_df = pd.DataFrame(results)
    print("\nHybrid recommender tuning results:")
    print(results_df)
    
    best_weight = results_df.loc[results_df['hit_rate'].idxmax()]['cf_weight']
    print(f"Best collaborative filtering weight: {best_weight}")
    
    return best_weight
