import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import './BudMan.css'; // Create a separate CSS file for styling

const BudMan = () => {
  const [budgets, setBudgets] = useState([]);

  useEffect(() => {
    const getBudgetsUrl = 'http://127.0.0.1:5000/api/v1/budget/';
    fetch(getBudgetsUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setBudgets(data.data);
      })
      .catch(error => {
        console.error('Error fetching the data:', error);
      });
  }, []);

  const deleteBudgetByIndex = (id) => {
    const deleteBudgetUrl = 'http://127.0.0.1:5000/api/v1/budget/';
    fetch(deleteBudgetUrl + id, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Server response was not ok');
        }
        console.log("deleted budget");
        setBudgets(budgets.filter(budget => budget.budget_id !== id));
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  return (
    <article className="budman-container">
      <section className="budman-header">
        <h1>Budget Management</h1>
        <div className="budman-actions">
          <button className="budman-button create-button">
            <NavLink to="/create-budget">Create New Budget</NavLink>
          </button>
          <button className="budman-button manage-button">
            <NavLink to="/category-managing">Manage Categories</NavLink>
          </button>
        </div>
      </section>

      {budgets.length > 0 ? (
        <section className="budget-list">
          {budgets.map((item) => (
            <div key={item.budget_id} className="budget-item">
              <div className="budget-details">
                <p className="budget-amount">Total Amount: £{item.total_amount}</p>
                <p className="budget-date">Start Date: {item.start_date}</p>
                <p className="budget-date">End Date: {item.end_date}</p>
              </div>
              <div className="budget-actions">
                <button className="budman-button edit-button">
                  <NavLink to={`/edit/${item.budget_id}`}>Edit</NavLink>
                </button>
                <button
                  className="budman-button delete-button"
                  onClick={() => deleteBudgetByIndex(item.budget_id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </section>
      ) : (
        <section className="no-budgets">
          <p>You have no budget plans.</p>
        </section>
      )}
    </article>
  );
};

export default BudMan;