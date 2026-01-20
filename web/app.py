from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import pickle
import os
import json
import sys

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load models and data when app starts
cf_model = None
hybrid_model = None
movies_df = None

def load_models():
    global cf_model, hybrid_model, movies_df
    try:
        # Ensure the models directory exists
        os.makedirs('models', exist_ok=True)
        
        if not os.path.exists('models/cf_model.pkl') or not os.path.exists('models/hybrid_model.pkl'):
            print("Model files don't exist. Please run 'python -m scripts.train' first")
            return False
            
        with open('models/cf_model.pkl', 'rb') as f:
            cf_model = pickle.load(f)
        with open('models/hybrid_model.pkl', 'rb') as f:
            hybrid_model = pickle.load(f)
            
        # Load movies data
        movies_df = pd.read_csv('data/ml-latest-small/movies.csv')
        print("Models and data loaded successfully")
        return True
    except Exception as e:
        print(f"Error loading models: {e}")
        print("Please run 'python -m scripts.train' first")
        return False


@app.route('/')
def index():
    # Ensure models are loaded
    global movies_df
    if movies_df is None:
        if not load_models():
            return render_template('error.html', 
                                  error="Models not loaded. Please run 'python -m scripts.train' first.")
    
    # Get a sample of movie titles for the UI
    sample_movies = movies_df.sample(min(50, len(movies_df)))[['movieId', 'title']].to_dict('records')
    return render_template('index.html', movies=sample_movies)


@app.route('/api/search')
def api_search():
    # Ensure models are loaded
    global movies_df
    if movies_df is None:
        load_models()
        
    query = request.args.get('q', '').lower()
    if not query or len(query) < 2:
        return jsonify([])
    
    # Filter movies by title
    mask = movies_df['title'].str.lower().str.contains(query)
    results = movies_df[mask].head(10)[['movieId', 'title']].to_dict('records')
    return jsonify(results)


@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    # Ensure models are loaded
    if cf_model is None or hybrid_model is None:
        if not load_models():
            return jsonify({"error": "Models not loaded. Run 'python -m scripts.train' first"}), 500
    
    try:
        data = request.json
        user_id = data.get('userId')
        movie_id = data.get('movieId')
        
        if not user_id and not movie_id:
            return jsonify({"error": "Please provide either userId or movieId"}), 400
        
        results = {}
        
        # User-based recommendations
        if user_id:
            try:
                user_id = int(user_id)
                cf_recs = cf_model.recommend_items(user_id, n_recommendations=10)
                if not cf_recs.empty:
                    cf_recs = cf_recs.merge(movies_df[['movieId', 'title']], on='movieId')
                    results['collaborative'] = cf_recs[['movieId', 'title', 'score']].to_dict('records')
                
                hybrid_recs = hybrid_model.recommend_items(user_id, n_recommendations=10)
                if not hybrid_recs.empty:
                    hybrid_recs = hybrid_recs.merge(movies_df[['movieId', 'title']], on='movieId')
                    results['hybrid'] = hybrid_recs[['movieId', 'title', 'score']].to_dict('records')
            except ValueError:
                return jsonify({"error": "User ID must be a valid integer"}), 400
        
        # Movie-based recommendations
        if movie_id:
            try:
                movie_id = int(movie_id)
                from src.recommender.models import ContentBasedFiltering
                cb_model = ContentBasedFiltering()
                cb_model.fit(get_movie_features(movies_df), movies_df)
                
                similar_movies = cb_model.recommend_similar_movies(movie_id, n_recommendations=10)
                if not similar_movies.empty:
                    similar_movies = similar_movies.merge(movies_df[['movieId', 'title']], on='movieId')
                    results['similar_movies'] = similar_movies[['movieId', 'title', 'similarity']].to_dict('records')
            except ValueError:
                return jsonify({"error": "Movie ID must be a valid integer"}), 400
        
        if not results:
            return jsonify({"message": "No recommendations found"}), 404
            
        return jsonify(results)
    except Exception as e:
        app.logger.error(f"Error in recommendations: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Helper function
def get_movie_features(movies):
    from src.recommender.data import get_movie_features
    return get_movie_features(movies)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.template_filter('truncate_title')
def truncate_title(title, length=30):
    return (title[:length] + '...') if len(title) > length else title

if __name__ == '__main__':
    # Load models at startup
    load_models()
    
    # Change port from default 5000 to 8080 to avoid conflicts
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
