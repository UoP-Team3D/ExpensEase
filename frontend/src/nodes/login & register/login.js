import React from 'react';
import { NavLink } from 'react-router-dom';
import './lrgrid.css';

const Login = () => {

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
                    <button class="contBut">Continue</button>
                </div>
                <div>
                    <NavLink to="/register">Register here</NavLink>
                </div>

            </section>
        </article>
    );

}

export default Login;