import React from 'react';
import { NavLink } from 'react-router-dom';
import './style.css';

const Header = () =>{
    return(
        <header>
            <ul>
                <li><NavLink to="/budget-managing">Manager</NavLink></li>
                <li><NavLink to="/scan">scan</NavLink></li>
                <li><NavLink to="/history">History</NavLink></li>
            </ul>
        </header>
    )

}
export default Header;