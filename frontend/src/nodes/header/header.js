import React from 'react';
import { NavLink } from 'react-router-dom';
import './style.css';

const Header = () =>{
    const logout = 'http://127.0.0.1:5000/api/v1/logout';

    const handleLogout = () => {
        fetch(logout, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include'
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            window.location.path = '/login'; // Redirect to login page on successful logout
          } else {
            alert('Logout failed. Please try again.');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('An error occurred. Please try again.');
        });
      };

    return(
        <header>
            <div class='navbar '>
            <ul>
                <li><NavLink to="/home"activeClassName='active'>Home</NavLink></li>
                <li><NavLink to="/budget-managing"activeClassName='active'>Manager</NavLink></li>
                <li><NavLink to="/scan"activeClassName='active'>Scan</NavLink></li>
                <li><NavLink to="/history"activeClassName='active'>History</NavLink></li>
                <li><NavLink to="/settings" activeClassName='active'>Settings</NavLink></li>
                <li><NavLink to="/" onClick={handleLogout}>Logout</NavLink></li>
            </ul>
            </div>
        </header>
    )

}
export default Header;