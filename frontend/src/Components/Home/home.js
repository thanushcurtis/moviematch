import React, { useState, useEffect } from 'react';
import './home.css';
import { useNavigate } from "react-router-dom";
function HomePage() {
    const [username, setUsername] = useState('');
    const [watchList, setWatchList] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        
        fetchUsername();
        fetchWatchList();
    }, []);

    const fetchUsername = async () => { 
        try 
        {
          const response = await fetch('/get_current_user/', 
          {
              method: 'GET',
              credentials: 'include'
              
          });
    
          const data = await response.json();
         
          if (data.username) {
          setUsername(data.first_name);
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

    const fetchWatchList = async () => {
        try{
            const response = await fetch('/get_watchlist/', {
                method: 'GET',
                credentials: 'include'
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setWatchList(data);
        


        }catch (error) {
            console.error('Failed to fetch WatchList:', error);
        } 
    };

    const handleMovieDetails = (movieId) => {
        
        console.log(movieId); 
        navigate('/movie-details', { state: { movieId: movieId } });
    };

    if(!username){
        return (
            <div className="main_page">
                <div className='main_wrapper'>
                    <div className='main_opening'>
                        <h1>Welcome to Moviematch</h1>
                        <p>Your personal guide to the ultimate movie-watching experience.</p>
                        <div>
                            <h1>About Moviematch</h1>
                            <ul>
                                <li>Finding your next watch made easy with personalized, curated movie recommendations.</li>
                                <li>Get suggestions based on your tastes</li>
                                <li>Utilizes keywords from your preferred movie reviews to find your next favorite movie.</li>
                            </ul>
                        </div>
                        <div>
                            <h1>How It Works</h1>
                            <p>In MovieMatch, the main factor for the recommendation of the
                                    movies will be extracting keywords from the reviews of the previously preferred movies
                                    and find those keywords in the movies that user haven't watched yet and recommend those movies
                                    along with other factors such as cast of the movie, genre, director, and viewing platforms.</p>
                        </div>
                        <div>
                            <h1>Ready to find your perfect movie match?</h1>
                            <div className='register_link'>
                                <p><a href="/register" >Register Now</a></p>
                                <p>Already have an account? <a href="/login">Log in</a></p>
                            </div>
                        </div>
                        <footer>
                            <p> Final Year Project - Thanushkumar Sasinthra Thilipkumar</p>
                        </footer>
                    </div>
                </div>
            </div>
        );
    };

    

    return (
        <div className="main_page">
            <div className='main_wrapper'>
                <h1>Welcome {username}!!</h1>
                <p> Please Find your WatchList Here</p>
                {watchList.length > 0 ? (
                    <div className='movies-grid'>
                        {watchList.map((movie, index) => (
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
                ) : (
                    <p>There are no movies in your watchlist. Check out recommendations and add them to your list!</p>
                )}
             </div>
        </div>

    );
};

export default HomePage;
