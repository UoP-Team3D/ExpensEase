import {React, useState, useEffect} from 'react';
import { NavLink } from 'react-router-dom';
import './lrgrid.css';

const Register = () => {
    const [errorMessage, setErrorMessage] = useState("");


    function val(){
     
      
            const url = "http://127.0.0.1:5000/api/v1/register";

            const fn = document.querySelector('#fname').value;
            const ln = document.querySelector('#lname').value;
            const un = document.querySelector('#usernReg').value;
            const mail = document.querySelector('#mailReg').value;
            const pw = document.querySelector('#passReg').value;
            const pin = document.querySelector('#pincode').value;

        
            
            const data = {
                username: un,
                password: pw,
                email: mail,
                first_name: fn,
                last_name: ln,
                pin: pin,                
            }

            console.log(JSON.stringify(data));

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
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

            window.location.href = '/login';
       
    }

    function event(){
        const regBut = document.getElementById("reg");
        regBut.addEventListener('click', val);
    }
   

    function init(){
        document.addEventListener('DOMContentLoaded',event)
    }



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
                    <input type="text" placeholder="username" id="usernReg" required></input>
                </div>
                <div>
                    <label>Email:</label>
                    <br/>
                    <input type="text" placeholder="e-mail" id="mailReg" required></input>
                </div>
                <div>
                    <label>Password:</label>
                    <br/>
                    <input type="password" placeholder="password" id="passReg" required></input>
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
                    <button className="contBut" id="reg" onClick={val}>Register</button>
                </div>
                <div>
                    <NavLink to="/login">Already registered?</NavLink>
                </div>

            </section>
        </article>
    );
}

export default Register;