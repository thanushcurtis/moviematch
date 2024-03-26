import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import './movieDetails.css'; 

function MovieDetails() {
  const location = useLocation();
  const [movieDetails, setMovieDetails] = useState(null);

  useEffect(() => {
    const { movieId } = location.state;
    const fetchMovieDetails = async () => {
      try {
        const response = await fetch(`/movie-details/${movieId}`);
        if (!response.ok) throw new Error('Failed to fetch');
        const data = await response.json();
        setMovieDetails(data);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchMovieDetails();
  }, [location.state]);

  if (!movieDetails) return <div>Loading...</div>;

  return (
    <div className='wrapper'>
        <div className="movie_details">
        <img src={movieDetails.poster_path} alt={`${movieDetails.title} Poster`} />
        <h2>{movieDetails.title} ({new Date(movieDetails.release_date).getFullYear()})</h2>
        <p>{movieDetails.overview}</p>
        <div>User Score: {movieDetails.user_score}</div>
        <h3>Cast:</h3>
        <ul>
            {movieDetails.cast.map((actor, index) => (
            <li key={index}>{actor}</li>
            ))}
        </ul>
        <h3>Keywords:</h3>
        <ul className="keywords">
            {movieDetails.keywords.map((keyword, index) => (
            <li key={index}>{keyword}</li>
            ))}
        </ul>
        </div>
    </div>
  );
}

export default MovieDetails;
