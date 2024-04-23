import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./nodes/header/header";
import Home from "./nodes/home/home";
import BudMan from "./nodes/budget manager/BudgetManager";
import History from "./nodes/history/history";
import Scan from "./nodes/scan/scan";
import Login from './nodes/login & register/login';
import Register from './nodes/login & register/register'
import CreateBudget from './nodes/create budget/createBudget';

export default function App() {
  
  const isLoginorRegPage = window.location.pathname === '/login' || window.location.pathname === '/register';
  if(window.location.pathname == '/'){
    window.location.pathname = '/login';
  }
  return (
    <>
      <BrowserRouter>
        {isLoginorRegPage?null : <Header/>}
        
        <Routes>
          <Route path="/login" element={<Login/>}></Route>
          <Route path="/register" element={<Register/>}></Route>
          <Route path="/home" element={<Home/>}/>
          <Route path="/budget-managing" element={<BudMan/>}/>
          <Route path="/create-budget" element={<CreateBudget/>}/>
          <Route path="/history" element={<History/>}/>
          <Route path="/scan" element={<Scan/>}/>
        </Routes>
      </BrowserRouter>
    </>
  );
}
