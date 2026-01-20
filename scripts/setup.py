import os
import shutil

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory already exists: {path}")

def setup_project_structure():
    """Create a well-organized project directory structure."""
    # Define directories to create
    directories = [
        'data',                  # Raw data files
        'models',                # Saved model files
        'web/static',            # Static files
        'web/static/images',     # Generated plots and images
        'web/static/css',        # CSS files
        'web/static/js',         # JavaScript files
        'web/templates',         # HTML templates
        'logs',                  # Log files
        'notebooks'              # Jupyter notebooks
    ]
    
    # Create directories
    for directory in directories:
        create_directory(directory)
    
    # Move existing files to appropriate locations
    files_to_move = [
        # (source, destination)
        ('analysis_notebook.ipynb', 'notebooks/analysis_notebook.ipynb'),
        # Add other files here that need to be moved
    ]
    
    for source, dest in files_to_move:
        if os.path.exists(source) and not os.path.exists(dest):
            shutil.copy2(source, dest)
            print(f"Moved {source} to {dest}")
    
    print("\nProject structure setup complete!")
    print("\nDirectory structure:")
    for directory in directories:
        print(f"- {directory}/")

if __name__ == "__main__":
    setup_project_structure()
