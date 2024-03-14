import React, { useState, useEffect } from 'react';
import "./recommendation.css";
function Recommendation() {
    const [genres, setGenres] = useState([]);
    const [selectedGenres, setSelectedGenres] = useState([]);
    const [recommendations, setRecommendations] = useState([]);

    // Fetch genres from the backend when the component mounts
    useEffect(() => {
        const fetchGenres = async () => {
            const url = '/get_genres/';

            try {
                const response = await fetch(url);
                const genreNames = await response.json(); // This now directly receives a list of genre names
                setGenres(genreNames);
            } catch (error) {
                console.error('Failed to fetch genres:', error);
            }
        };

        fetchGenres();
    }, []);

    // Handle genre selection
    const toggleGenreSelection = (genreName) => {
        setSelectedGenres(prevSelectedGenres => {
            if (prevSelectedGenres.includes(genreName)) {
                return prevSelectedGenres.filter(name => name !== genreName); // Unselect
            } else {
                return [...prevSelectedGenres, genreName]; // Select
            }
        });
    };

    // Function to fetch recommendations
    const fetchRecommendations = async () => {
        try {
            const response = await fetch('/get_recommendations/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ genres: selectedGenres }),
            });
            console.log(selectedGenres)

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            setRecommendations(data); // Set the recommendations in state
        } catch (error) {
            console.error('Failed to fetch recommendations:', error);
        }
    };

    return (
        <div className='wrapper' >
            <h1>Recommendation</h1>
            <div>
                {genres.map((genreName, index) => (
                    <button
                        key={index} // Changed to index since we no longer have genre.id
                        onClick={() => toggleGenreSelection(genreName)}
                        className={selectedGenres.includes(genreName) ? 'selected' : ''}
                    >
                        {genreName}
                    </button>
                ))}
            </div>
            <button onClick={fetchRecommendations}>Get Recommendations</button>
            <div>
                <h2>Movie Recommendations</h2>
                <ul>
                    {recommendations.map((movie, index) => (
                        <li key={index}>
                            <div>
                                <img src={movie.poster_path} alt={`${movie.name} Poster`} />
                                <div>
                                    <h3>{movie.name}</h3>
                                    <p>Year: {movie.year}</p>
                                </div>
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default Recommendation;
