import React,{ useState } from "react";
import "./LoginRegister.css";
import { useNavigate } from "react-router-dom";
import { FaUserCircle, FaLock } from "react-icons/fa";

function Login(){
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginSuccess, setLoginSuccess] = useState(false); // New state for tracking login success

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Replace with your API endpoint
    const response = await fetch('http://localhost:8000/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    if (response.status === 200) {
      setLoginSuccess(true); // Update state on successful login
    } else {
      alert('Login failed! Please check your credentials.');
    }
  };

  return (
    <div className="wrapper">
      <form onSubmit={handleSubmit}>
        <h2>Login</h2>
        <div className="input_box">
          <input 
            type="text" 
            placeholder="Username" 
            required 
            value={username} 
            onChange={(e) => setUsername(e.target.value)}
          />
          <FaUserCircle className="icon" />
        </div>
        <div className="input_box">
          <input 
            type="password" 
            placeholder="Password" 
            required 
            value={password} 
            onChange={(e) => setPassword(e.target.value)}
          />
          <FaLock className="icon" />
        </div>
        <div className="forgot_checkbox">
          <label><input type="checkbox"/> Remember me</label>
          <a href="#">Forgot Password?</a>
        </div>
        <button type="submit">Login</button>
        {loginSuccess && <p>Logged in successfully!</p>}
        <div className="register_link">
          <p>Don't have an account? <a href="/register">Register</a></p>
        </div>
      </form>
    </div>
  );
}

export default Login;