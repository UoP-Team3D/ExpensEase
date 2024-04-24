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
        e.preventDefault();  // Prevent form from refreshing the page on submit
        if (formData.password !== formData.confirmPassword) {
            setErrorMessage("Passwords do not match");
            return;
        }
        setErrorMessage("");

        const url = "http://127.0.0.1:5000/api/v1/register";
        const data = {
            username: formData.username,
            password: formData.password,
            email: formData.email,
            first_name: formData.firstName,
            last_name: formData.lastName,
            pin: formData.pin,
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
                alert("Error: " + data.message);
            } else {
                alert("Success: " + data.message);
                navigate('/login'); // Redirect to login page on successful registration
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: An error occurred. Please try again.');
        });
    };

    return (
        <article>
            <section className="lrGrid border">
                <form onSubmit={handleSubmit}>
                    <div>
                        <label>First name:</label>
                        <br/>
                        <input type="text" placeholder="first name" id="firstName" required onChange={handleChange} value={formData.firstName} />
                    </div>
                    <div>
                        <label>Last name:</label>
                        <br/>
                        <input type="text" placeholder="last name" id="lastName" required onChange={handleChange} value={formData.lastName} />
                    </div>
                    <div>
                        <label>Username:</label>
                        <br/>
                        <input type="text" placeholder="username" id="username" required onChange={handleChange} value={formData.username} />
                    </div>
                    <div>
                        <label>Email:</label>
                        <br/>
                        <input type="email" placeholder="e-mail" id="email" required onChange={handleChange} value={formData.email} />
                    </div>
                    <div>
                        <label>Password:</label>
                        <br/>
                        <input type="password" placeholder="password" id="password" required onChange={handleChange} value={formData.password} />
                    </div>
                    <div>
                        <label>Confirm password:</label>
                        <br/>
                        <p style={{ color: 'red' }}>{errorMessage}</p>
                        <input type="password" placeholder="confirm password" id="confirmPassword" required onChange={handleChange} value={formData.confirmPassword} />
                    </div>
                    <div>
                        <label>Pin:</label>
                        <br/>
                        <input type="password" pattern="[0-9]{4}" placeholder="pin" id="pin" maxLength="4" required onChange={handleChange} value={formData.pin} />
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
