from setuptools import setup, find_packages

setup(
    name="movie-recommender",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'scipy',
        'requests',
    ],
    description="Movie recommendation system using collaborative and content-based filtering",
    author="Ahmed Ikram",
)
