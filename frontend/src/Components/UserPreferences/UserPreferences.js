import React, { useState, useEffect } from 'react';

import { useNavigate } from "react-router-dom";
import './UserPreference.css';


function GenreSelection(){
    
    const [username, setUsername] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    const [movieDetails, setMovieDetails] = useState(null);
    const navigate = useNavigate();



    useEffect(() => {
        fetchUsername();
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


  const fetchMovieDetails = async () => {
    if (!searchQuery) return;
    try {
        const response = await fetch(`/get_movies/?query=${encodeURIComponent(searchQuery)}`);
        const data = await response.json();
        setMovieDetails(data);
        console.log("Movie details:", data);
    } catch (error) {
        console.error('Error:', error);
        setMovieDetails(null);
    }
};

const postWatchedMovie = async (movieId) => {
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
        // Handle response data or state updates here
    } catch (error) {
        console.error('Error posting watched movie:', error);
    }
};



return (
    <div>
        <div className='container'>
            
            <div className='wrapper'>
                <h2>Select Your Watched Movies</h2>
                <p>logged in as: {username}</p>
                <div className="input_box">
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="Search for a movie..."
                    />
    
                </div>
                <button onClick={fetchMovieDetails}>Search</button>
            </div>
            
            {movieDetails && (
                <div className='movie_details'>
                    <h3>{movieDetails.name} ({movieDetails.release_year})</h3>
                    <p>Movie ID: {movieDetails.id}</p>
                    {movieDetails.poster_path && (
                        <img src={movieDetails.poster_path} alt={movieDetails.name} />
                    )}
                    <button onClick={() => postWatchedMovie(movieDetails.id)} className='next_page_btn'>Mark as Watched</button>
                </div>
            )} 
            
        </div>
        <button onClick={() => navigate("/recommendation")} className="next_page_btn">Next Page</button>
       
    </div>
);

}

export default GenreSelection;
