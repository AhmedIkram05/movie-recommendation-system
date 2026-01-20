import pickle
import os
from src.recommender.data import load_data, prepare_data, get_movie_features
from src.recommender.models import CollaborativeFiltering, HybridRecommender
from src.recommender.tuning import tune_collaborative_filtering, tune_hybrid_weights

def main():
    print("Training and saving recommendation models...")
    
    # Load data
    ratings, movies = load_data()
    
    # Prepare data
    user_item_matrix, train_data, test_data = prepare_data(ratings)
    movie_features = get_movie_features(movies)
    
    # Create models directory if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')
    
    # Optional: Find optimal parameters
    print("Finding optimal parameters...")
    try:
        best_k = tune_collaborative_filtering(user_item_matrix, train_data, test_data, movies)
        best_weight = tune_hybrid_weights(user_item_matrix, movie_features, train_data, test_data, movies)
        
        # Convert best_k to an integer to avoid sklearn error
        best_k = int(best_k)
    except Exception as e:
        print(f"Error tuning parameters: {e}")
        best_k = 20
        best_weight = 0.7
    
    # Train models with optimal parameters
    print(f"Training final models with k={best_k}, cf_weight={best_weight}...")
    cf_model = CollaborativeFiltering(k=best_k)
    cf_model.fit(user_item_matrix)
    
    hybrid_model = HybridRecommender(cf_weight=best_weight)
    hybrid_model.fit(user_item_matrix, movie_features, movies, train_data)
    
    # Save models
    with open('models/cf_model.pkl', 'wb') as f:
        pickle.dump(cf_model, f)
        
    with open('models/hybrid_model.pkl', 'wb') as f:
        pickle.dump(hybrid_model, f)
    
    print("Models saved to 'models' directory")

if __name__ == "__main__":
    main()
