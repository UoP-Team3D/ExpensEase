import {React, useState, useEffect} from 'react';
import { NavLink } from 'react-router-dom';
import './lrgrid.css';

const Register = () => {
    const [errorMessage, setErrorMessage] = useState("");
    useEffect(() => {
    const val = () =>{
        let pass1 = document.getElementById("passLog").value;
        let pass2 = document.getElementById("passLogcon").value;

       
        if(pass1 === pass2){
            setErrorMessage('');
            console.log("register function here");
        } else {
            setErrorMessage('Passwords are not matching');
        }
    }
    const regBut = document.getElementById("reg");
        regBut.addEventListener('click', val);
        return () => {
            regBut.removeEventListener('click', val);
        };
    },  );
   


    return (
        <article>
            <section class="lrGrid border">
                <div>
                    <label>First name:</label>
                    <br/>
                    <input type="text" placeholder="first name" id="fname" required></input>
                </div>
                <div>
                    <label>Last name:</label>
                    <br/>
                    <input type="text" placeholder="last name" id="lname" required></input>
                </div>
                <div>
                    <label>Username:</label>
                    <br/>
                    <input type="text" placeholder="username" id="usernLog" required></input>
                </div>
                <div>
                    <label>Email:</label>
                    <br/>
                    <input type="text" placeholder="e-mail" id="mail" required></input>
                </div>
                <div>
                    <label>Password:</label>
                    <br/>
                    <input type="password" placeholder="password" id="passLog" required></input>
                </div>
                <div>
                    <label>Confirm password</label>
                    <br/>
                    <p style={{ color: 'red' }} id="alert">{errorMessage}</p>
                    <input type="password" placeholder="confirm password" id="passLogcon"required></input>                    
                </div>
                <div>
                    <label>Pin:</label>
                    <br/>
                    <input type="password" pattern="[0-9]{4}" placeholder="pin" id="pincode" maxlength="4" required></input>
                </div>
                
                <div>
                    <button class="contBut" id="reg">Register</button>
                </div>
                <div>
                    <NavLink to="/login">Already registered?</NavLink>
                </div>

            </section>
        </article>
    );
}

export default Register;