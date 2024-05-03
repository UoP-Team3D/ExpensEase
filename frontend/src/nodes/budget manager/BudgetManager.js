import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';

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
      headers: {'Content-Type': 'application/json'},
      credentials: 'include',
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Server response was not ok');
      }
      console.log("deleted budget");
      // Update the budgets state by removing the deleted budget
      setBudgets(budgets.filter(budget => budget.budget_id !== id));
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  return (
    <article>
      {budgets.length > 0 ? (
        <section>
          <button><NavLink to="/create-budget">Create new budget</NavLink></button>
          <button><NavLink to="/category-managing">Manage your categories</NavLink></button>
          <h1>List of your budgets:</h1>
          <ul>
            {budgets.map((item, index) => (
              <li key={item.budget_id}>
                <span>Total amount: £{item.total_amount}</span><br/>
                <span>Start date: {item.start_date}</span><br/>
                <span>End date: {item.end_date}</span><br/>
                <button>
                  <NavLink to={`/edit/${item.budget_id}`}>Edit</NavLink>
                </button>
                <button onClick={() => deleteBudgetByIndex(item.budget_id)}>Delete</button>
              </li>
            ))}
          </ul>
        </section>
      ) : (
        <h1>Create your first budget-plan</h1>
      )}
    </article>
  );
};

export default BudMan;