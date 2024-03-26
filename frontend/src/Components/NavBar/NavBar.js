import React from 'react';
import './NavBar.css';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();
  

  const handleLogout = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch('/logout/', { method: 'GET' });
      const data = await response.json();
      console.log(data.message); 
      navigate('/');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <nav className="navbar">
      <h4>Movie Recommendation System</h4>
      <div className="navbar-nav">
        <a href="/">Home</a>
        <a href="/genre-selection">Select Movies</a>
        <a href="/recommendation">Recommendations</a>
        <a href="/logout" onClick={handleLogout}>Logout</a>
      </div>
    </nav>



  );
};

export default Navbar;
