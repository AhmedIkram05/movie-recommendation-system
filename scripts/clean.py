import os
import subprocess
import sys

def run_command(command):
    print(f"Running: {command}")
    process = subprocess.run(command, shell=True, text=True, capture_output=True)
    if process.returncode != 0:
        print(f"Error: {process.stderr}")
        return False
    return True

def main():
    # Create .gitignore if it doesn't exist
    if not os.path.exists('.gitignore'):
        print("Creating .gitignore...")
        with open('.gitignore', 'w') as f:
            f.write("""
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# IDE
.idea/
.vscode/

# Model files (too large for GitHub)
models/*.pkl

# Generated files
*.png

# Cache
.cache/

# Jupyter
.ipynb_checkpoints/
""")
        run_command('git add .gitignore')
        run_command('git commit -m "Add .gitignore file"')
    
    # Create models directory if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')
    
    print("\nRemoveing large files from Git history...")
    run_command('git rm --cached models/*.pkl')
    run_command('git commit -m "Remove large model files from Git"')
    
    print("\nYou can now try pushing to GitHub again using:")
    print("git push -u origin main")
    
    print("\nNote: If you've already pushed these large files, you may need to force push:")
    print("git push -f -u origin main")
    print("\nWarning: Force pushing rewrites history and can cause issues for other collaborators.")

if __name__ == "__main__":
    main()
