import React, { useState, useEffect } from 'react';

import { useNavigate } from "react-router-dom";
import './UserPreference.css';


function GenreSelection(){
    
    const [username, setUsername] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    const [movieDetails, setMovieDetails] = useState(null);
    const [postMovie, setPostMovie] = useState(null);
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
        if(!response.ok){
            throw new Error('Movie not found');
        }
        const data = await response.json();
        setMovieDetails(data);
        console.log("Movie details:", data);
    } catch (error) {
        console.error('Error:', error);
        setMovieDetails("Movie not found given name");
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
        if(response.ok){
            setPostMovie('Movie marked as watched');
            console.log(postMovie);
        } else{
            setPostMovie('Failed to mark the movie as watched');
        }

    } catch (error) {
        console.error('Error posting watched movie:', error);
    }
};



return (
    <div >
        <div className='main_container'>
            <div className='user_wrapper'>
                <h1>Select Movies</h1>
                {!movieDetails && (
                <>
                    <p>Please Search for the movies you already watched or preferred</p>
                    <p>Keywords for your preferences will be generated from these movies</p>
                </>
                )}
                <div className="input_box">
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="Search for a movie..."
                    />
    
                </div>
                <button onClick={fetchMovieDetails} className="next_page_btn">Search</button>
            </div>
            {movieDetails && (
                <div className='movie_details'>
                    {typeof movieDetails === 'string' ? (
                        <p>{movieDetails}</p>
                    ) : (
                        <>
                        <h3>{movieDetails.name} ({movieDetails.release_year})</h3>
                        <p>Movie ID: {movieDetails.id}</p>
                        {movieDetails.poster_path && (
                            <img src={movieDetails.poster_path} alt={`${movieDetails.name} poster`} />
                        )}
                        <button onClick={() => postWatchedMovie(movieDetails.id)} className='next_page_btn'>
                            Mark as Watched
                        </button>
                        {postMovie && <p>{postMovie}</p>}
                        </>
                    )}
                </div>
            )} 
        </div>
        <button onClick={() => navigate("/recommendation")} className="next_page_btn">Next Page</button>
       
    </div>
);

}

export default GenreSelection;
