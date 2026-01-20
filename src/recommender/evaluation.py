import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

def precision_at_k(recommended_items, actual_items, k=5):
    """
    Calculate precision@k metric.
    """
    if len(recommended_items) > k:
        recommended_items = recommended_items[:k]
    
    # Count the number of recommended items that were actually relevant
    hits = len(set(recommended_items) & set(actual_items))
    
    # Calculate precision
    precision = hits / min(k, len(recommended_items)) if len(recommended_items) > 0 else 0
    
    return precision

def recall_at_k(recommended_items, actual_items, k=5):
    """
    Calculate recall@k metric.
    """
    if len(recommended_items) > k:
        recommended_items = recommended_items[:k]
    
    # Count the number of recommended items that were actually relevant
    hits = len(set(recommended_items) & set(actual_items))
    
    # Calculate recall
    recall = hits / len(actual_items) if len(actual_items) > 0 else 0
    
    return recall

def evaluate_recommendations(model, test_data, movies_df, threshold=3.5, k=5, verbose=True):
    """
    Evaluate recommendation model using precision and recall.
    
    Parameters:
    - model: Recommendation model with recommend_items method
    - test_data: DataFrame of test ratings
    - movies_df: DataFrame of movie metadata
    - threshold: Minimum rating to consider an item "liked"
    - k: Number of recommendations to evaluate
    - verbose: Whether to print detailed results
    """
    precision_scores = []
    recall_scores = []
    hit_rate = 0
    
    # Group test data by user
    user_groups = test_data.groupby('userId')
    test_users = test_data['userId'].unique()
    print(f"Evaluating on {len(test_users)} users")
    
    # Sample users for evaluation to avoid long processing time
    eval_users = np.random.choice(test_users, min(50, len(test_users)), replace=False)
    
    for user_id in eval_users:
        # Get user test data
        user_test_data = user_groups.get_group(user_id)
        
        # Skip users with too few ratings in test set
        if len(user_test_data) < 2:
            continue
        
        # Get items the user liked in the test set
        actual_liked = user_test_data[user_test_data['rating'] >= threshold]['movieId'].tolist()
        if not actual_liked:
            continue
            
        # Get recommendations for this user
        try:
            recs = model.recommend_items(user_id, n_recommendations=k)
            if recs.empty:
                continue
                
            recommended_items = recs['movieId'].tolist()
            
            # Calculate precision and recall
            prec = precision_at_k(recommended_items, actual_liked, k)
            rec = recall_at_k(recommended_items, actual_liked, k)
            
            precision_scores.append(prec)
            recall_scores.append(rec)
            
            if prec > 0:
                hit_rate += 1
                
            # Print detailed results for some users
            if verbose and len(precision_scores) <= 3:
                print(f"\nUser {user_id} evaluation:")
                # Get movie titles for better output
                rec_titles = movies_df[movies_df['movieId'].isin(recommended_items[:5])]['title'].tolist()
                actual_titles = movies_df[movies_df['movieId'].isin(actual_liked[:5])]['title'].tolist()
                
                print(f"  Recommended movies: {rec_titles}")
                print(f"  Actually liked: {actual_titles}")
                print(f"  Precision: {prec:.4f}, Recall: {rec:.4f}")
                
        except Exception as e:
            print(f"Error evaluating user {user_id}: {e}")
    
    # Calculate average metrics
    avg_precision = np.mean(precision_scores) if precision_scores else 0
    avg_recall = np.mean(recall_scores) if recall_scores else 0
    hit_rate = hit_rate / len(eval_users) if eval_users.size > 0 else 0
    
    if verbose:
        print(f"\nEvaluation results on {len(precision_scores)} valid users:")
        print(f"Hit Rate: {hit_rate:.4f} (proportion of users with at least one relevant recommendation)")
        print(f"Precision@{k}: {avg_precision:.4f}")
        print(f"Recall@{k}: {avg_recall:.4f}")
    
    return avg_precision, avg_recall, hit_rate
