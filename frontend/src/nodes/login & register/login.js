import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import './lrgrid.css';

const Login = () => {
    const [credentials, setCredentials] = useState({
        username: '',
        password: ''
    });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (event) => {
        const { id, value } = event.target;
        setCredentials(prevCredentials => ({
            ...prevCredentials,
            [id]: value
        }));
    };

    const continueLogin = (event) => {
      event.preventDefault();
  
      const url = "http://127.0.0.1:5000/api/v1/login";
  
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include', 
        body: JSON.stringify(credentials)
      })
      .then(response => {
          if (!response.ok) {
              throw new Error('Wrong username or password'); 
          }
          return response.json();
      })
      .then(data => {
        if (data.success) {
          navigate('/home'); 
        } else {
          setError(data.message); 
        }
      })
      .catch(error => {
        setError(error.message); 
        console.error('Error:', error);
      });
  };

    return (
        <article>
            <section className="lrGrid border">
                <div className="logo-container">
                    <img src="/Logo.png" alt="ExpensEase Logo" className="logo" />
                </div>
                <form onSubmit={continueLogin}>
                    <div>
                        <label>Username:</label>
                        <input type="text" placeholder="username" id="username" required onChange={handleChange} value={credentials.username} />
                    </div>
                    <div>
                        <label>Password:</label>
                        <input type="password" placeholder="password" id="password" required onChange={handleChange} value={credentials.password} />
                    </div>
                    <div>
                        <button type="submit" className="contBut">Continue</button>
                    </div>
                    {error && <p style={{ color: 'red' }}>{error}</p>} 
                    <div>
                        <NavLink to="/register">Register here</NavLink>
                    </div>
                </form>
            </section>
        </article>
    );
}

export default Login;
