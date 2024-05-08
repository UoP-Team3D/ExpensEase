import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import './lrgrid.css';

const Register = () => {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        pin: ''
    });
    const [errorMessage, setErrorMessage] = useState("");
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.id]: e.target.value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();  
        if (formData.password !== formData.confirmPassword) {
            setErrorMessage("Passwords do not match");
            return;
        }

        const url = "http://127.0.0.1:5000/api/v1/register";
        const data = {
            username: formData.username,
            password: formData.password,
            email: formData.email,
            first_name: formData.firstName,
            last_name: formData.lastName,
            pin: '0000',  
        };

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                setErrorMessage(data.message);
            } else {
                navigate('/login');  
            }
        })
        .catch(error => {
            console.error('Error:', error);
            setErrorMessage('An error occurred. Please try again.');
        });
    };

    return (
        <article>
            <section className="lrGrid border">
                <div className="logo-container-reg">
                    <img src="/Logo.png" alt="ExpensEase Logo" className="logo-reg" />
                </div>
                <form onSubmit={handleSubmit}>
                    <div>
                        <label>First name:</label>
                        <input type="text" placeholder="first name" id="firstName" required onChange={handleChange} value={formData.firstName} />
                    </div>
                    <div>
                        <label>Last name:</label>
                        <input type="text" placeholder="last name" id="lastName" required onChange={handleChange} value={formData.lastName} />
                    </div>
                    <div>
                        <label>Username:</label>
                        <input type="text" placeholder="username" id="username" required onChange={handleChange} value={formData.username} />
                    </div>
                    <div>
                        <label>Email:</label>
                        <input type="email" placeholder="e-mail" id="email" required onChange={handleChange} value={formData.email} />
                    </div>
                    <div>
                        <label>Password:</label>
                        <input type="password" placeholder="password" id="password" required onChange={handleChange} value={formData.password} />
                    </div>
                    <div>
                        <label>Confirm password:</label>
                        {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
                        <input type="password" placeholder="confirm password" id="confirmPassword" required onChange={handleChange} value={formData.confirmPassword} />
                    </div>
                    <div>
                        <button type="submit" className="contBut">Register</button>
                    </div>
                    <div>
                        <NavLink to="/login">Already registered?</NavLink>
                    </div>
                </form>
            </section>
        </article>
    );
}

export default Register;
