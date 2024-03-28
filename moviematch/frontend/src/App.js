import './App.css';
import Login from './Components/LoginRegister/Login';
import Register from './Components/LoginRegister/Register';
import GenreSelection from './Components/UserPreferences/UserPreferences';  
import Recommendation from './Components/MainPage/recommendation';
import MovieDetails from './Components/MovieDetails/movieDetails';
import Navbar from './Components/NavBar/NavBar'; 
import HomePage from './Components/Home/home';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"; 

function App() {
  return (
    <Router>
      <Navbar /> 
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} /> 
        <Route path="/register" element={<Register />} />
        <Route path="/genre-selection" element={<GenreSelection />} />
        <Route path="/recommendation" element={<Recommendation />} />
        <Route path="/movie-details" element={<MovieDetails />} />

      </Routes>
    </Router>
  );
}

export default App;
