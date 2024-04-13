import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import './movieDetails.css'; 

function MovieDetails() {
  const location = useLocation();
  const [movieDetails, setMovieDetails] = useState(null);
  const [response, setResponeMessage] = useState('');
  const [isInWatchlist, setIsInWatchlist] = useState(false);
  const { movieId } = location.state;

  useEffect(() => {
    
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

    const checkWatchlist = async () => {
      try{
        const respone = await fetch('/get_watchlist_ids/', {
          method: 'GET',
          headers: {
            'Cache-Control': 'no-cache', 
          },
          credentials: 'include'
        });
        if (!respone.ok) {
          throw new Error(`HTTP error! status: ${respone.status}`);
        }
        const data = await respone.json();
        const isMovieInWatchlist = data.includes(movieId.toString());
        setIsInWatchlist(isMovieInWatchlist);
      } catch (error) {
        console.error('Failed to fetch watchlist:', error);
      }
    };

    fetchMovieDetails();
    checkWatchlist();
  }, [movieId]);

  if (!movieDetails) return <div>Loading...</div>;

  const watchListDisplay = async () => {
    const url = isInWatchlist ? `/movie-details/remove_from_watchlist/${movieId}` : `/movie-details/post_watchlist/${movieId}`;
    const method = isInWatchlist ? 'DELETE' : 'POST';

    try {
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setResponeMessage(data.message);
      setIsInWatchlist(!isInWatchlist); 
    } catch (error) {
      console.error(`Failed to ${isInWatchlist ? 'remove from' : 'add to'} watchlist:`, error);
      setResponeMessage(`Failed to ${isInWatchlist ? 'remove from' : 'add to'} watchlist.`);
    }
  };

  const postWatchedMovie = async () => {
    try {
        console.log("Posting watched movie with ID:", movieId);
        const response = await fetch('/post_watched_movie/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ movieId }),
            credentials: 'include',
        });

        const data = await response.json();
        console.log("Watched movie posted successfully", data);
        if(response.ok){
          setResponeMessage('Movie marked as watched');
        } else{
          setResponeMessage('Failed to mark the movie as watched');
        }
      
    } catch (error) {
        console.error('Error posting watched movie:', error);
    }
  };

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
          <div className="button-container">
            <button onClick={() => watchListDisplay()}>{
              isInWatchlist ? 'Remove from WatchList' : 'Add to WatchList'}
            </button>
            <button onClick={() => postWatchedMovie()} >Mark as Watched</button>
          </div>
          {response && <div>{response}</div>}
        </div>
    </div>
  );
}

export default MovieDetails;
