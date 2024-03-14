import './App.css';
import Login from './Components/LoginRegister/Login';
import Register from './Components/LoginRegister/Register';
import GenreSelection from './Components/UserPreferences/UserPreferences';  
import Recommendation from './Components/MainPage/recommendation';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"; 

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/genre-selection" element={<GenreSelection />} />
        <Route path="/recommendation" element={<Recommendation />} />

      </Routes>
    </Router>
  );
}

export default App;
