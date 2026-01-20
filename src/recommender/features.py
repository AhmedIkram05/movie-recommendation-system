import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def enhance_movie_features(movies_df, tags_path='data/ml-latest-small/tags.csv'):
    """
    Enhance movie features by incorporating tags and better genre processing
    """
    # Load tags if available
    try:
        tags_df = pd.read_csv(tags_path)
        # Aggregate tags for each movie
        tags_by_movie = tags_df.groupby('movieId')['tag'].apply(
            lambda x: ' '.join(x.str.lower())
        ).reset_index()
    except:
        tags_by_movie = pd.DataFrame({'movieId': [], 'tag': []})
        print("Tags file not found. Using only genres for content features.")
    
    # Process genres to use as text
    movies_df['genres_text'] = movies_df['genres'].str.replace('|', ' ')
    
    # Merge with tags
    movie_content = movies_df.merge(tags_by_movie, on='movieId', how='left')
    movie_content['tag'] = movie_content['tag'].fillna('')
    
    # Combine tags and genres into a single text field
    movie_content['content'] = (movie_content['genres_text'] + ' ' + 
                               movie_content['tag'] + ' ' + 
                               movie_content['title'])
    
    # Use TF-IDF to convert text to feature vectors
    tfidf = TfidfVectorizer(stop_words='english', min_df=2)
    tfidf_matrix = tfidf.fit_transform(movie_content['content'])
    
    # Calculate similarity matrix
    similarity = cosine_similarity(tfidf_matrix)
    
    # Create a mapping from movieId to index
    movie_idx = {movie_id: i for i, movie_id in enumerate(movie_content['movieId'])}
    
    return movie_content, similarity, movie_idx
