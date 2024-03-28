import React from 'react';
import './home.css'; 

const HomePage = () => {
    return (
        <div className="container">

            <header>
                <h1>Welcome to Moviematch</h1>
                <p>Your personal guide to the ultimate movie-watching experience.</p>
            </header>
            <section>
                <h2>About Moviematch</h2>
                <ul>
                    <li>Finding your next watch made easy with personalized, curated movie recommendations.</li>
                    <li>Get suggestions based on your tastes</li>
                    <li>Utilizes keywords from your preferred movie reviews to find your next favorite movie.</li>
                </ul>
            </section>
            <section>
                <h2>How It Works</h2>
                <p>In MovieMatch, the main factor for the recommendation of the
                    movies will be extracting keywords from the reviews of the previously preferred movies
                     and find those keywords in the movies that user haven't watched yet and recommend those movies
                    along with other factors such as cast of the movie, genre, director, and viewing platforms.</p>
            </section>
            <section>
                <h2>Ready to find your perfect movie match?</h2>
                <div className="register_link">
                <p><a href="/register" >Register Now</a></p>
                <p>Already have an account? <a href="/login">Log in</a></p>
                </div>
        
                
            </section>
            <footer>
                <p> Final Year Project - Thanushkumar Sasinthra Thilipkumar</p>
            </footer>
        </div>
    );
};

export default HomePage;
