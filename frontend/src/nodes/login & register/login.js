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
      event.preventDefault(); // Prevent form from submitting traditionally
    
      const url = "http://127.0.0.1:5000/api/v1/login";
    
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include', // Add this line to include credentials (cookies)
        body: JSON.stringify(credentials)
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert(data.message); // Display login success message
            navigate('/home');
            const token = data.session;
            localStorage.setItem('token', token);
            alert(token);
          } else {
            setError(data.message); // Set error message from server
            alert(data.message); // Optionally remove this line if you handle errors inline
          }
        })
        .catch(error => {
          setError('An error occurred. Please try again later.');
          console.error('Error:', error);
        });
    };

    return (
        <article>
            <section className="lrGrid border">
                <form onSubmit={continueLogin}>
                    <div>
                        <label>Username:</label>
                        <br/>
                        <input type="text" placeholder="username" id="username" required onChange={handleChange} value={credentials.username} />
                    </div>
                    <div>
                        <label>Password:</label>
                        <br/>
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
