document.addEventListener('DOMContentLoaded', function() {
    // Initialize any components when the page loads
    console.log('Movie Recommendation System loaded');
});

function getUserRecommendations() {
    const userId = document.getElementById('userId').value;
    if (!userId) {
        alert('Please enter a User ID');
        return;
    }
    
    // Show loading indicator
    const loading = document.getElementById('loading');
    loading.style.display = 'block';
    const container = document.getElementById('recommendationsContainer');
    container.innerHTML = '';
    
    fetch('/api/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userId: userId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Server responded with an error');
        }
        return response.json();
    })
    .then(data => {
        loading.style.display = 'none';
        displayRecommendations(data);
    })
    .catch(error => {
        loading.style.display = 'none';
        console.error('Error:', error);
        document.getElementById('recommendationsContainer').innerHTML = 
            `<div class="alert alert-danger">Error getting recommendations: ${error.message}</div>`;
    });
}

function getSimilarMovies() {
    const movieId = document.getElementById('movieSelect').value;
    if (!movieId) {
        alert('Please select a movie');
        return;
    }
    
    // Show loading indicator
    const loading = document.getElementById('loading');
    loading.style.display = 'block';
    const container = document.getElementById('recommendationsContainer');
    container.innerHTML = '';
    
    fetch('/api/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ movieId: movieId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Server responded with an error');
        }
        return response.json();
    })
    .then(data => {
        loading.style.display = 'none';
        displayRecommendations(data);
    })
    .catch(error => {
        loading.style.display = 'none';
        console.error('Error:', error);
        document.getElementById('recommendationsContainer').innerHTML = 
            `<div class="alert alert-danger">Error getting similar movies: ${error.message}</div>`;
    });
}

function displayRecommendations(data) {
    const container = document.getElementById('recommendationsContainer');
    container.innerHTML = '';
    
    if (data.collaborative) {
        container.innerHTML += '<h3 class="mb-4"><i class="fas fa-users me-2"></i>Collaborative Filtering Recommendations</h3>';
        container.innerHTML += '<div class="row" id="cfRecs"></div>';
        
        const cfContainer = document.getElementById('cfRecs');
        data.collaborative.forEach(movie => {
            cfContainer.innerHTML += `
                <div class="col-md-4 mb-4">
                    <div class="movie-card">
                        <div class="movie-title">${movie.title}</div>
                        <div class="movie-score">
                            <i class="fas fa-star text-warning me-1"></i> 
                            Score: <span class="score">${movie.score.toFixed(2)}</span>
                        </div>
                    </div>
                </div>
            `;
        });
    }
    
    if (data.hybrid) {
        container.innerHTML += '<h3 class="mt-5 mb-4"><i class="fas fa-magic me-2"></i>Hybrid Recommendations</h3>';
        container.innerHTML += '<div class="row" id="hybridRecs"></div>';
        
        const hybridContainer = document.getElementById('hybridRecs');
        data.hybrid.forEach(movie => {
            hybridContainer.innerHTML += `
                <div class="col-md-4 mb-4">
                    <div class="movie-card">
                        <div class="movie-title">${movie.title}</div>
                        <div class="movie-score">
                            <i class="fas fa-star text-warning me-1"></i> 
                            Score: <span class="score">${movie.score.toFixed(2)}</span>
                        </div>
                    </div>
                </div>
            `;
        });
    }
    
    if (data.similar_movies) {
        container.innerHTML += '<h3 class="mt-5 mb-4"><i class="fas fa-film me-2"></i>Similar Movies</h3>';
        container.innerHTML += '<div class="row" id="similarMovies"></div>';
        
        const similarContainer = document.getElementById('similarMovies');
        data.similar_movies.forEach(movie => {
            similarContainer.innerHTML += `
                <div class="col-md-4 mb-4">
                    <div class="movie-card">
                        <div class="movie-title">${movie.title}</div>
                        <div class="movie-score">
                            <i class="fas fa-thumbs-up text-success me-1"></i> 
                            Similarity: <span class="score">${movie.similarity.toFixed(2)}</span>
                        </div>
                    </div>
                </div>
            `;
        });
    }
    
    if (!data.collaborative && !data.hybrid && !data.similar_movies) {
        container.innerHTML = '<div class="alert alert-warning">No recommendations found.</div>';
    }
}
