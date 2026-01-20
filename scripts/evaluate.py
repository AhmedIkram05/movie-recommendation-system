import sys

# Try to import dependencies and provide helpful message if missing
try:
    import pandas as pd
    from src.recommender.data import load_data, prepare_data, get_movie_features
    from src.recommender.models import CollaborativeFiltering, ContentBasedFiltering, HybridRecommender
    from src.recommender.evaluation import evaluate_recommendations
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Please install required dependencies with:")
    print("pip install -r requirements.txt")
    sys.exit(1)

def main():
    print("MovieLens Recommendation System")
    print("="*30)
    
    # Load data
    try:
        ratings, movies = load_data()
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)
    
    # Prepare data
    user_item_matrix, train_data, test_data = prepare_data(ratings)
    movie_features = get_movie_features(movies)
    
    print("Preparing recommender models...")
    # Initialize models
    cf_model = CollaborativeFiltering(k=10)
    cb_model = ContentBasedFiltering()
    hybrid_model = HybridRecommender(cf_weight=0.7)
    
    # Train models
    print("\nTraining collaborative filtering model...")
    cf_model.fit(user_item_matrix)
    
    print("Training content-based filtering model...")
    cb_model.fit(movie_features, movies)
    
    print("Training hybrid recommendation model...")
    hybrid_model.fit(user_item_matrix, movie_features, movies, train_data)
    
    # Example recommendations
    print("\n--- Example Recommendations ---")
    
    # Get a random user
    random_user = ratings['userId'].sample(1).iloc[0]
    print(f"Recommendations for user {random_user}:")
    
    # Get recommendations from each model
    cf_recommendations = cf_model.recommend_items(random_user, n_recommendations=5)
    hybrid_recommendations = hybrid_model.recommend_items(random_user, n_recommendations=5)
    
    # Add movie titles to recommendations
    if not cf_recommendations.empty:
        cf_recommendations = cf_recommendations.merge(movies[['movieId', 'title']], on='movieId')
        print("\nCollaborative filtering recommendations:")
        for _, row in cf_recommendations.iterrows():
            print(f"- {row['title']} (score: {row['score']:.2f})")
    
    if not hybrid_recommendations.empty:
        hybrid_recommendations = hybrid_recommendations.merge(movies[['movieId', 'title']], on='movieId')
        print("\nHybrid recommendations:")
        for _, row in hybrid_recommendations.iterrows():
            print(f"- {row['title']} (score: {row['score']:.2f})")
    
    # Get content-based recommendations for a movie this user has rated highly
    user_ratings = ratings[ratings['userId'] == random_user]
    if not user_ratings.empty:
        top_rated_movie = user_ratings.loc[user_ratings['rating'].idxmax()]['movieId']
        movie_title = movies[movies['movieId'] == top_rated_movie]['title'].iloc[0]
        
        print(f"\nMovies similar to {movie_title}:")
        cb_recommendations = cb_model.recommend_similar_movies(top_rated_movie, n_recommendations=5)
        
        if not cb_recommendations.empty:
            cb_recommendations = cb_recommendations.merge(movies[['movieId', 'title']], on='movieId')
            for _, row in cb_recommendations.iterrows():
                print(f"- {row['title']} (similarity: {row['similarity']:.2f})")
    
    # Evaluate models
    print("\n--- Model Evaluation ---")
    print("Evaluating collaborative filtering model...")
    cf_precision, cf_recall, cf_hit_rate = evaluate_recommendations(cf_model, test_data, movies, k=10)
    
    print("\nEvaluating hybrid recommendation model...")
    hybrid_precision, hybrid_recall, hybrid_hit_rate = evaluate_recommendations(hybrid_model, test_data, movies, k=10)
    
    # Store metrics for visualization
    try:
        from src.recommender.visualization import plot_model_comparison, plot_rating_distribution, plot_user_activity
        
        # Create visualizations
        print("\nGenerating visualizations...")
        plot_rating_distribution(ratings)
        
        metrics_dict = {
            'Collaborative': (cf_precision, cf_recall, cf_hit_rate),
            'Hybrid': (hybrid_precision, hybrid_recall, hybrid_hit_rate)
        }
        plot_model_comparison(metrics_dict)
        plot_user_activity(ratings)
        
        print("Visualizations saved to current directory.")
    except ImportError:
        print("Visualization modules not available. Skipping visualizations.")

if __name__ == "__main__":
    main()
