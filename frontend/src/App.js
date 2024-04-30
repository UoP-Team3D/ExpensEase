import React from 'react';
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import Header from "./nodes/header/header";
import Home from "./nodes/home/home";
import BudMan from "./nodes/budget manager/BudgetManager";
import History from "./nodes/history/history";
import Scan from "./nodes/scan/scan";
import Login from './nodes/login & register/login';
import Register from './nodes/login & register/register'
import CreateBudget from './nodes/budget manager/create budget/createBudget';
import Settings from './nodes/settings/settings';
import EditBudget from './nodes/budget manager/edit budget/editBudget';

const Layout = () => {
  const location = useLocation();
  const isLoginorRegPage = location.pathname === '/login' || location.pathname === '/register';
  return (
    <>
        {isLoginorRegPage?null : <Header/>}
        
        <Routes>
          <Route path="/login" element={<Login/>}></Route>
          <Route path="/register" element={<Register/>}></Route>
          <Route path="/home" element={<Home/>}/>
          <Route path="/budget-managing" element={<BudMan/>}/>
          <Route path="/create-budget" element={<CreateBudget/>}/>
          <Route path="/history" element={<History/>}/>
          <Route path="/scan" element={<Scan/>}/>
          <Route path="/settings" element={<Settings />} />
          <Route path="/edit/:id" element={<EditBudget />} />
        </Routes>
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  );
}
