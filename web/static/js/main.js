const PLACEHOLDER_IMG = '/static/images/placeholders/poster_placeholder.png';
const OMDB_API_KEY = 'f6b59f0b'; // User provided key

document.addEventListener('DOMContentLoaded', function() {
    console.log('App Loaded');
    setupAutocomplete();
});

// Setup Autocomplete
function setupAutocomplete() {
    const container = document.getElementById('searchContainer'); // We need to add this to HTML
    if (!container) return;

    const input = document.getElementById('movieSearchInput');
    const resultsDiv = document.createElement('div');
    resultsDiv.className = 'search-results';
    container.appendChild(resultsDiv);

    let timeout = null;

    input.addEventListener('input', function() {
        clearTimeout(timeout);
        const query = this.value;
        
        if (query.length < 2) {
            resultsDiv.style.display = 'none';
            return;
        }

        timeout = setTimeout(() => {
            fetch(`/api/search?q=${encodeURIComponent(query)}`)
                .then(res => res.json())
                .then(data => {
                    resultsDiv.innerHTML = '';
                    if (data.length > 0) {
                        data.forEach(movie => {
                            const div = document.createElement('div');
                            div.className = 'search-item';
                            div.textContent = movie.title;
                            div.onclick = () => {
                                input.value = movie.title;
                                input.dataset.movieId = movie.movieId; // Store ID
                                resultsDiv.style.display = 'none';
                            };
                            resultsDiv.appendChild(div);
                        });
                        resultsDiv.style.display = 'block';
                    } else {
                        resultsDiv.style.display = 'none';
                    }
                });
        }, 300); // Debounce
    });

    // Close on click outside
    document.addEventListener('click', function(e) {
        if (!container.contains(e.target)) {
            resultsDiv.style.display = 'none';
        }
    });
}

function getUserRecommendations() {
    const userId = document.getElementById('userId').value;
    if (!userId) {
        alert('Please enter a User ID');
        return;
    }
    fetchRecommendations({ userId: userId });
}

function getSimilarMovies() {
    // Get ID from dataset (set by autocomplete) or select
    const input = document.getElementById('movieSearchInput');
    const movieId = input.dataset.movieId;
    
    if (!movieId) {
        alert('Please select a movie from the search results');
        return;
    }
    fetchRecommendations({ movieId: movieId });
}

function fetchRecommendations(payload) {
    const loading = document.getElementById('loading');
    const container = document.getElementById('recommendationsContainer');
    
    loading.style.display = 'block';
    container.innerHTML = '';

    fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        loading.style.display = 'none';
        displayRecommendations(data);
    })
    .catch(err => {
        loading.style.display = 'none';
        container.innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
    });
}

function displayRecommendations(data) {
    const container = document.getElementById('recommendationsContainer');
    container.innerHTML = '';

    // Async function to fetch poster
    const getPoster = async (title, imgElement) => {
        try {
            // Clean title (remove year in parenthesis)
            const cleanTitle = title.replace(/\s*\(\d{4}\)/, '');
            const url = `https://www.omdbapi.com/?t=${encodeURIComponent(cleanTitle)}&apikey=${OMDB_API_KEY}`;
            const res = await fetch(url);
            const meta = await res.json();
            
            if (meta.Response === 'True' && meta.Poster !== 'N/A') {
                imgElement.style.backgroundImage = `url('${meta.Poster}')`;
            }
        } catch (e) {
            console.warn('Failed to fetch poster for', title);
        }
    };

    // Helper to create sections
    const createSection = (title, movies) => {
        if (!movies) return '';
        
        // Create section container
        const sectionTitle = document.createElement('h3');
        sectionTitle.className = 'mb-3 text-white';
        sectionTitle.textContent = title;
        container.appendChild(sectionTitle);
        
        const grid = document.createElement('div');
        grid.className = 'movie-grid';
        
        movies.forEach(m => {
            const card = document.createElement('div');
            card.className = 'movie-card';
            card.onclick = () => alert(`Movie ID: ${m.movieId}`);
            
            // Poster Div
            const posterDiv = document.createElement('div');
            posterDiv.className = 'movie-poster';
            // Set initial placeholder
            posterDiv.style.background = `center/cover url('https://via.placeholder.com/300x450/333/fff?text=${encodeURIComponent(m.title)}')`;
            
            // Fetch real poster
            getPoster(m.title, posterDiv);
            
            const infoDiv = document.createElement('div');
            infoDiv.className = 'movie-info';
            
            infoDiv.innerHTML = `
                <div class="movie-title" title="${m.title}">${m.title}</div>
                <div class="movie-meta">
                    <span class="score-badge">${(m.score || m.similarity * 50 || 0).toFixed(1)} Match</span>
                </div>
            `;
            
            card.appendChild(posterDiv);
            card.appendChild(infoDiv);
            grid.appendChild(card);
        });
        
        container.appendChild(grid);
        
        const hr = document.createElement('hr');
        hr.className = 'my-5 border-secondary';
        container.appendChild(hr);
    };

    if (data.hybrid) createSection('Top Picks For You (Hybrid)', data.hybrid);
    if (data.similar_movies) createSection('Because You Liked Certain Movies (Content)', data.similar_movies);
    if (data.collaborative) createSection('Popular With Similar Users (Collaborative)', data.collaborative);
}
