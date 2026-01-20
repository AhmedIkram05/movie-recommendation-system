import importlib
import sys

def check_dependencies():
    """Check that all required packages are installed."""
    required_packages = ['pandas', 'numpy', 'sklearn', 'scipy', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Error: Missing required packages:", ', '.join(missing_packages))
        print("Please install them using:")
        print("pip install -r requirements.txt")
        return False
    
    return True

if __name__ == "__main__":
    if check_dependencies():
        print("All dependencies are installed.")
    else:
        sys.exit(1)
