import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import './style.css';

const Header = () => {
  const [showMenu, setShowMenu] = useState(false);

  const handleLogout = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/logout', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });
      const data = await response.json();
      if (data.success) {
        window.location.href = '/login'; // Use href instead of path
      } else {
        alert('Logout failed. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    }
  };

  const handleToggleMenu = () => {
    setShowMenu(!showMenu);
  };

  return (
    <header>
      <nav className='navbar'>
        <div>
        <img src="/Logo.png" alt="Logo" style={{ width: '50px', height: '50px' }} />
        </div>
        <ul className={`nav-links ${showMenu ? 'show' : ''}`}>
          <li><NavLink to="/home" activeClassName='active'>Home</NavLink></li>
          <li><NavLink to="/budget-managing" activeClassName='active'>Manager</NavLink></li>
          <li><NavLink to="/scan" activeClassName='active'>Scan</NavLink></li>
          <li><NavLink to="/history" activeClassName='active'>History</NavLink></li>
          <li><NavLink to="/settings" activeClassName='active'>Settings</NavLink></li>
          <li><NavLink to="/" onClick={handleLogout}>Logout</NavLink></li>
        </ul>
        <div className="hamburger-menu" onClick={handleToggleMenu}>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
        </div>
      </nav>
    </header>
  );
}

export default Header;