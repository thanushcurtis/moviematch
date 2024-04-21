import React, { useState, useEffect } from 'react';
import "./recommendation.css";
import { useNavigate } from "react-router-dom";

function Recommendation() {
    const [genres, setGenres] = useState([]);
    const [username, setUsername] = useState('');
    const [selectedGenres, setSelectedGenres] = useState([]);
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(false);
    const [progress, setProgress] = useState('Waiting for updates...');
    const navigate = useNavigate();

    useEffect(() => {
        const storedGenres = localStorage.getItem('genres');
        const storedRecommendations = localStorage.getItem('recommendations');
        if (storedGenres) {
            setGenres(JSON.parse(storedGenres));
        } else {
            fetchGenres();
        }
        if (storedRecommendations) {

            setRecommendations(JSON.parse(storedRecommendations));
        }
        fetchUsername();
    }, []);

    const fetchGenres = async () => {
        const url = '/get_genres/';
        const response = await fetch(url);
        if (response.ok) {
            const genreNames = await response.json();
            setGenres(genreNames);
            localStorage.setItem('genres', JSON.stringify(genreNames));
        } else {
            console.error('Failed to fetch genres');
        }
    };

    const fetchUsername = async () => {
        const response = await fetch('/login_status/', { method: 'GET', credentials: 'include' });
        const data = await response.json();
        setUsername(data.username || null);
    };

    const handleFetchRecommendations = () => {
        if (selectedGenres.length === 0) {
            alert('Please select at least one genre.');
            return;
        }
        setLoading(true);
        setProgress("Starting recommendation process...");
        const genreQuery = selectedGenres.map(genre => `genres=${encodeURIComponent(genre)}`).join('&');
        const url = `/get_recommendations/?${genreQuery}`;
        const events = new EventSource(url);
    
        events.addEventListener('progress', function(event) {
            setProgress(event.data);
        });
    
        events.addEventListener('data', function(event) {
            setRecommendations(JSON.parse(event.data));
            localStorage.setItem('recommendations', event.data);
            setLoading(false);
            events.close();
        });
    
        events.onerror = function(event) {
            if (event.eventPhase === EventSource.CLOSED) {
                console.error('SSE closed');
            } else {
                console.error('SSE error occurred: ', event);
            }
            setLoading(false);
            setProgress("Connection failed.");
            events.close();
    
           
            if (event.target && event.target.readyState === EventSource.CLOSED) {
                console.error('SSE connection was closed by the server');
            } else if (event.target && event.target.readyState === EventSource.CONNECTING) {
                console.error('SSE connection is reconnecting');
            } else if (event.target && event.target.readyState === EventSource.OPEN) {
                console.error('SSE connection is open but encountered an error');
            }
        };
    };
    

    const toggleGenreSelection = (genreName) => {
        setSelectedGenres(prev => prev.includes(genreName) ? prev.filter(name => name !== genreName) : [...prev, genreName]);
    };

    const handleMovieDetails = (movieId) => {
        navigate('/movie-details', { state: { movieId } });
    };

    if (!username) {
        return (
            <div>
                <p>User not logged in</p>
                <button className='next_page_btn' onClick={() => navigate('/login')}>Login</button>
            </div>
        );
    }

    return (
        <div className='wrapper'>
            <h1>Genres</h1>
            <p>Select the genres you like to get movie recommendations</p>
            <div className="genre-buttons">
                {genres.map((genreName, index) => (
                    <button key={index} onClick={() => toggleGenreSelection(genreName)}
                        className={selectedGenres.includes(genreName) ? 'selected' : ''}>
                        {genreName}
                    </button>
                ))}
            </div>
            <button className="get-recommendations" onClick={handleFetchRecommendations}>Get Recommendations</button>
            {loading && <p>{progress}</p>}
            {!loading && (
                <div className='movie-recommendations'>
                    <h2>Movie Recommendations</h2>
                    <div className="movies-grid">
                        {recommendations.map((movie, index) => (
                            <div className="movie-item" key={index}>
                                <img src={movie.poster_path} alt={`${movie.name} Poster`} />
                                <div>
                                    <h3>{movie.name}</h3>
                                    <p>{movie.year}</p>
                                    <button onClick={() => handleMovieDetails(movie.id)}>Movie Details</button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default Recommendation;