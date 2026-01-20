import os
import argparse
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description='Run Movie Recommendation System Components')
    parser.add_argument('--download', action='store_true', help='Download the dataset')
    parser.add_argument('--train', action='store_true', help='Train and save the models')
    parser.add_argument('--evaluate', action='store_true', help='Evaluate model performance')
    parser.add_argument('--visualize', action='store_true', help='Create visualizations')
    parser.add_argument('--web', action='store_true', help='Start web interface')
    parser.add_argument('--all', action='store_true', help='Run all components')
    parser.add_argument('--port', type=int, default=8080, help='Port for web interface')
    parser.add_argument('--setup', action='store_true', help='Set up project directory structure')
    parser.add_argument('--clean', action='store_true', help='Clean temporary files')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    # Set up project structure if requested
    if args.setup:
        subprocess.run([sys.executable, "-m", "scripts.setup"])
    
    # Clean cache files if requested
    if args.clean:
        from src.recommender.utils import clean_cache_files
        clean_cache_files()
    
    if args.download or args.all:
        print("Downloading dataset...")
        subprocess.run([sys.executable, "-m", "scripts.download"])
    
    if args.train or args.all:
        print("Training and saving models...")
        subprocess.run([sys.executable, "-m", "scripts.train"])
    
    if args.evaluate or args.all:
        print("Evaluating models...")
        subprocess.run([sys.executable, "-m", "scripts.evaluate"])
    
    if args.visualize or args.all:
        print("Creating visualizations...")
        try:
            from src.recommender.visualization import plot_rating_distribution, plot_model_comparison, plot_user_activity
            from src.recommender.data import load_data
            
            ratings, _ = load_data()
            plot_rating_distribution(ratings)
            plot_user_activity(ratings)
            print("Visualizations created and saved to static/images directory.")
        except ImportError as e:
            print(f"Error creating visualizations: {e}")
            print("Make sure matplotlib and seaborn are installed.")
    
    if args.web or args.all:
        print("Starting web interface...")
        if not os.path.exists('models/cf_model.pkl') or not os.path.exists('models/hybrid_model.pkl'):
            print("Models not found. Training models first...")
            subprocess.run([sys.executable, "-m", "scripts.train"])
        
        try:
            # Use the custom port
            port = args.port
            print(f"Starting web interface on port {port}...")
            
            # Set environment variable for Flask to use the specified port
            os.environ['FLASK_RUN_PORT'] = str(port)
            
            subprocess.run([sys.executable, "-m", "web.app"])
        except KeyboardInterrupt:
            print("Web interface stopped.")

if __name__ == "__main__":
    main()
