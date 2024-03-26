import React, { useState } from "react";
import './LoginRegister.css';
import { useNavigate } from "react-router-dom";
import { FaUserCircle, FaLock, FaEnvelope } from "react-icons/fa";

function Register() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        if(password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }
        const response = await fetch('http://127.0.0.1:5000/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: email, name: name, password: password }),
        });
        try {
            const data = await response.json();
            if(response.status === 201) {
                navigate("/login", { replace: true });
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Error parsing JSON:', error);
        }
    };
    

    return (
        <div className="wrapper">
            <form onSubmit={handleSubmit}>
                <h2>Register</h2>
                <div className="input_box">
                    <input 
                        type="text" 
                        placeholder="Name" 
                        required 
                        value={name} 
                        onChange={(e) => setName(e.target.value)} 
                    />
                    <FaUserCircle className="icon" />
                </div>
                <div className="input_box">
                    <input 
                        type="email" 
                        placeholder="Email" 
                        required 
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)} 
                    />
                    <FaEnvelope className="icon" />
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
                <div className="input_box">
                    <input 
                        type="password" 
                        placeholder="Confirm Password" 
                        required 
                        value={confirmPassword} 
                        onChange={(e) => setConfirmPassword(e.target.value)} 
                    />
                    <FaLock className="icon" />
                </div>
                <button type="submit">Register</button>
                <div className="register_link">
                    <p>Already have an account? <a href="/login"> Login </a></p>
                </div>
            </form>
        </div>
    );
}

export default Register;
