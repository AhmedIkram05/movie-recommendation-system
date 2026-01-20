#!/usr/bin/env python3
import sys
import os

# Add the project root to the python path if running directly
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.recommender.utils import download_movielens_dataset
    download_movielens_dataset()
