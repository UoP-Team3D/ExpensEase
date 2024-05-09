import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import Header from "./nodes/header/header";
import Home from "./nodes/home/home";
import BudMan from "./nodes/budget manager/BudgetManager";
import History from "./nodes/history/history";
import Scan from "./nodes/scan/scan";
import Login from './nodes/login & register/login';
import Register from './nodes/login & register/register';
import CreateBudget from './nodes/budget manager/create budget/createBudget';
import Settings from './nodes/settings/settings';
import EditBudget from './nodes/budget manager/edit budget/editBudget';
import CatMan from './nodes/budget manager/category manager/CategoryManger';
import socket from './socket';
import ProtectedRoute from './ProtectedRoute';

const Layout = () => {
  const location = useLocation();
  const isLoginorRegPage = location.pathname === '/login' || location.pathname === '/register';

  useEffect(() => {
    socket.connect();
    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <>
      {isLoginorRegPage ? null : <Header />}
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/home"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        <Route
          path="/budget-managing"
          element={
            <ProtectedRoute>
              <BudMan />
            </ProtectedRoute>
          }
        />
        <Route
          path="/create-budget"
          element={
            <ProtectedRoute>
              <CreateBudget />
            </ProtectedRoute>
          }
        />
        <Route
          path="/history"
          element={
            <ProtectedRoute>
              <History />
            </ProtectedRoute>
          }
        />
        <Route
          path="/scan"
          element={
            <ProtectedRoute>
              <Scan />
            </ProtectedRoute>
          }
        />
        <Route
          path="/settings"
          element={
            <ProtectedRoute>
              <Settings />
            </ProtectedRoute>
          }
        />
        <Route
          path="/edit/:id"
          element={
            <ProtectedRoute>
              <EditBudget />
            </ProtectedRoute>
          }
        />
        <Route
          path="/category-managing"
          element={
            <ProtectedRoute>
              <CatMan />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate replace to="/login" />} />
      </Routes>
    </>
  );
};

export default function App() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  );
}