import React, { useState, useEffect } from 'react';
import './../general.css';

const RingPieChart = ({ categoryId }) => {
  const [budget, setBudget] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBudgetByCategory = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/budget/category/${categoryId}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include'
        });

        if (!response.ok) {
          throw new Error('Budget not found');
        }
        const json = await response.json();
        setBudget(json.data[0]);
      } catch (error) {
        console.error('Failed to fetch budget:', error);
      } finally {
        setLoading(false);
      }
    };

    if (categoryId) {
      fetchBudgetByCategory();
    }
  }, [categoryId]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!budget) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <svg width="200" height="200" viewBox="0 0 200 200">
          <circle
            r="70"
            cx="100"
            cy="100"
            fill="transparent"
            stroke="#E0E0E0"
            strokeWidth="40"
            strokeDasharray="440"
          />
        </svg>
        <div className="budget-text" style={{ color: '#888' }}>
          You don't have a budget for this category!
        </div>
      </div>
    );
  }

  const { total_amount, current_amount, end_date } = budget;
  const spentAmount = total_amount - current_amount;
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const remainingPercentage = (current_amount / total_amount) * 100;
  const spentPercentage = (spentAmount / total_amount) * 100;

  const budgets = [
    { color: '#4CAF50', percentage: remainingPercentage },
    { color: '#F44336', percentage: spentPercentage }
  ];

  let accumulatedOffset = 0;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <svg width="200" height="200" viewBox="0 0 200 200">
        {budgets.map((budget, index) => {
          const dashArray = (budget.percentage / 100) * circumference;
          const dashOffset = -accumulatedOffset;
          accumulatedOffset += dashArray;

          return (
            <circle
              key={index}
              r={radius}
              cx="100"
              cy="100"
              fill="transparent"
              stroke={budget.color}
              strokeWidth="40"
              strokeDasharray={`${dashArray} ${circumference - dashArray}`}
              strokeDashoffset={dashOffset}
              transform="rotate(-90 100 100)"
            />
          );
        })}
      </svg>
      <div className="budget-text">
        You have £{current_amount.toFixed(2)}/£{total_amount.toFixed(2)} budget left until {end_date}
      </div>
    </div>
  );
};
const CategorySelector = ({ onCategoryChange }) => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/category/', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include'
        });

        if (!response.ok) {
          throw new Error('Failed to retrieve categories');
        }
        const json = await response.json();
        setCategories(json.data);
      } catch (error) {
        console.error('Error fetching categories:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  if (loading) {
    return <div>Loading categories...</div>;
  }

  return (
    <select onChange={e => onCategoryChange(e.target.value)} defaultValue="">
      <option value="" disabled>Select your category</option>
      {categories.map(category => (
        <option key={category.category_id} value={category.category_id}>
          {category.category_name}
        </option>
      ))}
    </select>
  );
};

const LatestScans = () => {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchExpenses = async () => {
      try {
        // Fetch the latest 3 expenses
        const queryParams = new URLSearchParams({
          sort_by: 'date',
          sort_order: 'desc',
          page: 1,
          per_page: 3,
        });

        const response = await fetch(`http://127.0.0.1:5000/api/v1/expense/?${queryParams}`,{
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include'
        });
        if (!response.ok) {
          throw new Error('Expenses could not be retrieved');
        }
        const json = await response.json();
        if (json.success) {
          setScans(json.data); // Set the retrieved expenses as the new scans
        }
      } catch (error) {
        console.error('Failed to fetch expenses:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchExpenses();
  }, []);

  if (loading) {
    return <div>Loading expenses...</div>;
  }

  return (
    <div className="latest-scans-container">
      <div className="latest-scans-header">Latest Scans:</div>
      <div className="latest-scans-table">
        <div className="table-header">
          <span>DATE/TIME</span>
          <span className="where-column">WHERE?</span>
          <span>AMOUNT</span>
        </div>
        {scans.length === 0 ? (
          <div className="table-row no-expenses-message">
            <span colSpan="3">You have no expenses yet!</span>
          </div>
        ) : (
          scans.map((expense, index) => (
            <div className="table-row" key={index}>
              <span>{expense.date}</span>
              <span className="where-column">{expense.category}</span>
              <span>£{expense.amount}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

const OverallBudgetChart = () => {
  const [overallBudget, setOverallBudget] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOverallBudget = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/budget/', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include'
        });

        if (!response.ok) {
          throw new Error('Failed to fetch overall budget');
        }
        const json = await response.json();
        const budgets = json.data;
        const totalAmount = budgets.reduce((sum, budget) => sum + budget.total_amount, 0);
        const currentAmount = budgets.reduce((sum, budget) => sum + budget.current_amount, 0);
        setOverallBudget({ total_amount: totalAmount, current_amount: currentAmount });
      } catch (error) {
        console.error('Failed to fetch overall budget:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchOverallBudget();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!overallBudget) {
    return <div>Overall budget not found</div>;
  }

  const { total_amount, current_amount } = overallBudget;
  const spentAmount = total_amount - current_amount;
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const remainingPercentage = (current_amount / total_amount) * 100;
  const spentPercentage = (spentAmount / total_amount) * 100;

  const budgets = [
    { color: '#4CAF50', percentage: remainingPercentage },
    { color: '#F44336', percentage: spentPercentage }
  ];

  let accumulatedOffset = 0;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <svg width="200" height="200" viewBox="0 0 200 200">
        {budgets.map((budget, index) => {
          const dashArray = (budget.percentage / 100) * circumference;
          const dashOffset = -accumulatedOffset;
          accumulatedOffset += dashArray;

          return (
            <circle
              key={index}
              r={radius}
              cx="100"
              cy="100"
              fill="transparent"
              stroke={budget.color}
              strokeWidth="40"
              strokeDasharray={`${dashArray} ${circumference - dashArray}`}
              strokeDashoffset={dashOffset}
              transform="rotate(-90 100 100)"
            />
          );
        })}
      </svg>
      <div className="budget-text">
        You have £{current_amount.toFixed(2)}/£{total_amount.toFixed(2)} overall budget
      </div>
    </div>
  );
};

const Home = () => {
  const [selectedCategoryId, setSelectedCategoryId] = useState(null);

  return (
    <article>
      <div className="welcome-message">
        <h1>Welcome to ExpensEase!</h1>
        <h3>Manage your finances, categorize your receipts, and take control of your spending.</h3>
      </div>
  
      <div className="grid">
        <div className="chart-container">
          {selectedCategoryId ? (
            <RingPieChart categoryId={selectedCategoryId} />
          ) : (
            <OverallBudgetChart />
          )}
  
          <div className="chart-dropdown">
            <CategorySelector onCategoryChange={setSelectedCategoryId} />
          </div>
        </div>
  
        <div >
          <LatestScans />
        </div>
      </div>
    </article>
  );
};

export default Home;