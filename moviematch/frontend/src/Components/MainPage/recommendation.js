import React, { useState, useEffect } from 'react';
import "./recommendation.css";
import { useNavigate } from "react-router-dom";

function Recommendation() {
    const [genres, setGenres] = useState([]);
    const [username, setUsername] = useState('');
    const [selectedGenres, setSelectedGenres] = useState([]);
    const [recommendations, setRecommendations] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetchUsername();
        const fetchGenres = async () => {
            const url = '/get_genres/';
            try {
                const response = await fetch(url);
                const genreNames = await response.json();
                setGenres(genreNames);
            } catch (error) {
                console.error('Failed to fetch genres:', error);
            }
        };

        fetchGenres();
    }, []);

    const fetchUsername = async () => {
        try 
        {
          const response = await fetch('/login_status/', 
          {
              method: 'GET',
              credentials: 'include'
              
          });
    
          const data = await response.json();
          console.log("Response:", data);
    
          if (data.username) {
  
          console.log("Session Username:", data.username);
          setUsername(data.username);
          } 
          else
          {
              console.log("User is not logged in.");
              setUsername(null);
          }
        } catch (error) {
          console.error('Error:', error);
          setUsername(null);
        }
    };

    if (!username) {
    
        return (
            <div>
                <p>User not logged in</p>
                <button className='next_page_btn' onClick={() => navigate('/login')}>Login</button>
            </div>
        );
    }

    

    const toggleGenreSelection = (genreName) => {
        setSelectedGenres(prevSelectedGenres => {
            if (prevSelectedGenres.includes(genreName)) {
                return prevSelectedGenres.filter(name => name !== genreName);
            } else {
                return [...prevSelectedGenres, genreName];
            }
        });
    };

    const fetchRecommendations = async () => {
        try {
            const response = await fetch('/get_recommendations/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ genres: selectedGenres }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            setRecommendations(data);
        } catch (error) {
            console.error('Failed to fetch recommendations:', error);
        }
    };

   
    const handleMovieDetails = (movieId) => {
        
        console.log(movieId); 
        navigate('/movie-details', { state: { movieId: movieId } });
    };

    return (
        <div className='wrapper'>
            <h1>Genres</h1>
            <p>Select the genres you like to get movie recommendations</p>
            <div className="genre-buttons">
                {genres.map((genreName, index) => (
                    <button
                        key={index}
                        onClick={() => toggleGenreSelection(genreName)}
                        className={selectedGenres.includes(genreName) ? 'selected' : ''}
                    >
                        {genreName}
                    </button>
                ))}
            </div>
            <button className="get-recommendations" onClick={fetchRecommendations}>Get Recommendations</button>
            <div className='movie-recommendations'>
                <h2>Movie Recommendations</h2>
                <div className="movies-grid">
                    {recommendations.map((movie, index) => (
                        <div className="movie-item" key={index}>
                            <img src={movie.poster_path} alt={`${movie.name} Poster`} />
                            <div>
                                <h3>{movie.name}</h3>
                                <p> {movie.year}</p>
                                <button onClick={() => handleMovieDetails(movie.id)}>Movie Details</button>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default Recommendation;
