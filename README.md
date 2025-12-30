# AI Movie Recommendation System

## 🚀 Overview

This project implements a comprehensive movie recommendation system using the MovieLens dataset. It explores various recommendation techniques including collaborative filtering, content-based filtering, and hybrid approaches to provide personalized movie suggestions. The system includes a Flask-based web interface for users to interact with the recommendations and visualize the underlying data.

## 🧠 Tech Stack

- **Core**: Python, Flask
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: scikit-Learn, SciPy
- **Visualization**: Matplotlib, Seaborn

## 📊 Features

- **Collaborative Filtering**: Recommends movies based on user similarity patterns and past ratings.
- **Content-Based Filtering**: Suggests movies with similar attributes (genres, tags) to what a user likes.
- **Hybrid Recommendation**: Combines collaborative and content-based methods to overcome limitations like the cold-start problem.
- **Interactive Web UI**: A user-friendly interface to get recommendations by user ID or movie title.
- **Data Visualization**: Tools to analyze rating distributions, user activity, and model performance metrics.

## 📈 Results

The models were evaluated using standard metrics like Hit Rate and Precision@k:

- **Collaborative Filtering**: Achieved ~78% hit rate and ~0.22 precision@10.
- **Hybrid Model**: Achieved ~74% hit rate and ~0.23 precision@10.

## 🧪 How to Run

1. **Clone the repository**

   ```bash
   git clone https://github.com/AhmedIkram05/movie-recommendation-system.git
   cd movie-recommendation-system
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Download Data & Train Models**
   You can do this in one step using the runner script:

   ```bash
   python run.py --download --train
   ```

   *Note: This will download the MovieLens dataset and train the models, saving them to the `models/` directory.*

4. **Run the Web Interface**

   ```bash
   python run.py --web
   ```

   Open your browser and navigate to `http://localhost:8080` to use the recommender.

## 🛠️ Advanced Usage

- **Evaluate Models**: `python run.py --evaluate`
- **Generate Visualizations**: `python run.py --visualize`
- **Clean Temporary Files**: `python run.py --clean`
