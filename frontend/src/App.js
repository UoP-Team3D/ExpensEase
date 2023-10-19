import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Log from "./pages/log/log";
import Scan from "./pages/scan/scan"


export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/"/>
        <Route path="/log" element={<Log/>}/>
        <Route path="/scan" element={<Scan/>}/>
      </Routes>
    </BrowserRouter>
  );
}
