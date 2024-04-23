import React from 'react';
import { NavLink } from 'react-router-dom';
import './lrgrid.css';

const Login = () => {

    function continueLogin(){
        const usern = document.querySelector('#usernLog');
        const passw = document.querySelector('#passLog');

        const url = "http://127.0.0.1:5000/api/v1/login";

        const data ={
            username: usern,
            password: passw
        }
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: data
        })
        .then(response => {
            if (!response.ok) {
                alert("Server error!");
            }
            return response.json();
        })
        .then(data => {
            alert("Success: ", data);
        })
        .catch(error => {
            alert("Error: ", error);
        })

        window.location.href = '/home';
    }
    return (
        <article>
            <section class="lrGrid border">
                <div>
                    <label>Username:</label>
                    <br/>
                    <input type="text" placeholder="username" id="usernLog"required></input>
                </div>
                <div>
                    <label>Password:</label>
                    <br/>
                    <input type="text" placeholder="password" id="passLog"required></input>
                </div>
                <div>
                    <button class="contBut" id="continue" onClick={continueLogin}>Continue</button>
                </div>
                <div>
                    <NavLink to="/register">Register here</NavLink>
                </div>

            </section>
        </article>
    );

}

export default Login;