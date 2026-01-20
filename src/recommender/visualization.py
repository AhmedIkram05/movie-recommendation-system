import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Ensure the images directory exists
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def plot_rating_distribution(ratings, save_path='web/static/images'):
    """Plot distribution of ratings."""
    ensure_dir(save_path)
    
    plt.figure(figsize=(10, 6))
    sns.countplot(x='rating', data=ratings)
    plt.title('Distribution of Ratings')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    
    # Save the plot
    file_path = os.path.join(save_path, 'ratings_distribution.png')
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return file_path

def plot_user_activity(ratings, save_path='web/static/images'):
    """Plot user activity (number of ratings per user)."""
    ensure_dir(save_path)
    
    user_counts = ratings.groupby('userId').size().reset_index(name='counts')
    
    plt.figure(figsize=(12, 6))
    sns.histplot(user_counts['counts'], kde=True, bins=30)
    plt.title('Distribution of Ratings per User')
    plt.xlabel('Number of Ratings')
    plt.ylabel('Count of Users')
    
    # Save the plot
    file_path = os.path.join(save_path, 'user_activity.png')
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return file_path

def plot_model_comparison(metrics_dict, save_path='web/static/images'):
    """Plot comparison of model metrics."""
    ensure_dir(save_path)
    
    # Create DataFrame from metrics dictionary
    models = list(metrics_dict.keys())
    precision_values = [metrics_dict[model][0] for model in models]
    recall_values = [metrics_dict[model][1] for model in models]
    hit_rate_values = [metrics_dict[model][2] for model in models]
    
    metrics_df = pd.DataFrame({
        'Model': models + models + models,
        'Metric': ['Precision@10'] * len(models) + ['Recall@10'] * len(models) + ['Hit Rate'] * len(models),
        'Value': precision_values + recall_values + hit_rate_values
    })
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Metric', y='Value', hue='Model', data=metrics_df)
    plt.title('Comparison of Recommendation Models')
    plt.ylabel('Score')
    plt.ylim(0, 1)
    plt.legend(title='Model')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save the plot
    file_path = os.path.join(save_path, 'model_comparison.png')
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return file_path

# Additional visualization functions can be added here
