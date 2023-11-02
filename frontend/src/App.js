import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./nodes/header/header"
import Home from "./nodes/home/home"
import BudMan from "./nodes/budget manager/BudgetManager"
import History from "./nodes/history/history"
import Scan from "./nodes/scan/scan"


export default function App() {
  return (
    <>
      <Header/>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home/>}/>
          <Route path="/budget-managning" element={<BudMan/>}/>
          <Route path="/history" element={<History/>}/>
          <Route path="/scan" element={<Scan/>}/>
        </Routes>
      </BrowserRouter>
    </>
  );
}
