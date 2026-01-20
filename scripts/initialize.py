import subprocess
import sys
import os

def main():
    """Initialize the project by running all setup scripts."""
    print("Initializing Movie Recommendation System project...")
    
    # Run setup_project.py to create directory structure
    print("\n1. Setting up project structure...")
    subprocess.run([sys.executable, "-m", "scripts.setup"])
    
    # Download data if needed
    print("\n2. Checking data availability...")
    if not os.path.exists('data/ml-latest-small/movies.csv'):
        print("   Data not found. Downloading dataset...")
        subprocess.run([sys.executable, "-m", "scripts.download"])
    else:
        print("   Data already exists.")
    
    # Train and save models if needed
    print("\n3. Checking model availability...")
    if not os.path.exists('models/cf_model.pkl') or not os.path.exists('models/hybrid_model.pkl'):
        print("   Models not found. Training models...")
        subprocess.run([sys.executable, "-m", "scripts.train"])
    else:
        print("   Models already exist.")
    
    print("\n4. Creating visualizations...")
    subprocess.run([sys.executable, "run.py", "--visualize"])
    
    print("\nInitialization complete! You can now run the system with:")
    print("python run.py --web")

if __name__ == "__main__":
    main()
