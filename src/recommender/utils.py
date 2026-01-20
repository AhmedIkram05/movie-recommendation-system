import os
import logging
import pickle
import shutil
import requests
import zipfile
import io

def setup_logging(log_file='logs/recommendation_system.log'):
    """Set up logging configuration."""
    # Ensure logs directory exists
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger('recommendation_system')

def save_model(model, filename):
    """Save model to file."""
    # Ensure models directory exists
    model_dir = os.path.dirname(filename)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    with open(filename, 'wb') as f:
        pickle.dump(model, f)
    
    return os.path.exists(filename)

def load_model(filename):
    """Load model from file."""
    if not os.path.exists(filename):
        return None
    
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    
    return model

def clean_cache_files():
    """Clean temporary cache files."""
    # Remove __pycache__ directories
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            try:
                shutil.rmtree(os.path.join(root, '__pycache__'))
                print(f"Removed {os.path.join(root, '__pycache__')}")
            except:
                pass

def download_movielens_dataset():
    """Download the MovieLens dataset."""
    # Create data directory
    if not os.path.exists('data'):
        os.makedirs('data')

    # Download MovieLens 100K dataset
    print("Downloading MovieLens dataset...")
    url = 'https://files.grouplens.org/datasets/movielens/ml-latest-small.zip'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        
        # Extract files
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall('data')
        
        # Verify extraction
        expected_files = ['ratings.csv', 'movies.csv']
        extracted_dir = 'data/ml-latest-small'
        
        for file in expected_files:
            if not os.path.exists(os.path.join(extracted_dir, file)):
                print(f"Error: Expected file {file} not found after extraction.")
                return False
                
        print('Dataset downloaded successfully!')
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading dataset: {e}")
        return False
    except zipfile.BadZipFile:
        print("Error: Downloaded file is not a valid zip file.")
        return False

