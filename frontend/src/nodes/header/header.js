import React from 'react';
import { NavLink } from 'react-router-dom';
import './style.css';

const Header = () =>{
    return(
        <header>
            <div class='navbar '>
            <ul>
                <li><NavLink to="/budget-managing"activeClassName='active'>Manager</NavLink></li>
                <li><NavLink to="/scan"activeClassName='active'>scan</NavLink></li>
                <li><NavLink to="/history"activeClassName='active'>History</NavLink></li>
            </ul>
            </div>
        </header>
    )

}
export default Header;