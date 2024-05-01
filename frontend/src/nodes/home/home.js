import React, { useState, useEffect } from 'react';
import './../general.css';

const RingPieChart = ({ budgetId }) => {
  const [budget, setBudget] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBudget = async () => {
      try {
        const startDate = new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0];
        const endDate = new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0).toISOString().split('T')[0];

        const response = await fetch(`http://127.0.0.1:5000/api/v1/budget/${budgetId}`,{
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include'
        });

        if (!response.ok) {
          throw new Error('Budget not found');
        }
        const json = await response.json();
        if (json.data.start_date === startDate && json.data.end_date === endDate) {
          setBudget(json.data);
        }
      } catch (error) {
        console.error('Failed to fetch budget:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchBudget();
  }, [budgetId]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!budget) {
    return <div>Budget not found for this month.</div>;
  }

  const totalBudget = budget.total_amount;
  const remainingBudget = budget.current_amount;
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const remainingPercentage = (remainingBudget / totalBudget) * 100;
  const spentPercentage = 100 - remainingPercentage;

  const budgets = [
    { color: '#4CAF50', percentage: remainingPercentage }, // Green for remaining budget
    { color: '#F44336', percentage: spentPercentage }, // Red for spent budget
  ];

  let accumulatedOffset = 0; // Initialize accumulated offset

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <svg width="200" height="200" viewBox="0 0 200 200">
        {budgets.map((budget, index) => {
          const dashArray = (budget.percentage / 100) * circumference;
          const dashOffset = -accumulatedOffset;
          accumulatedOffset += dashArray; // Update accumulatedOffset for the next segment

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
        You have £{remainingBudget}/£{totalBudget} budget left this month
      </div>
    </div>
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

        const response = await fetch(`http://127.0.0.1:5000/api/v1/expense/?${queryParams}`);
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
        {scans.map((expense, index) => (
          <div className="table-row" key={index}>
            <span>{expense.date}</span>
            <span className="where-column">{expense.category}</span>
            <span>£{expense.amount}</span>
          </div>
         ))}
      </div>
    </div>
  );
};

const Home = () => {
  const budgetId = 1; // Example budget ID, you can set this based on your app's logic

  return (
    <article>
      <div className="grid see-outline">
        {/* Use the RingPieChart by referencing it directly since it's in the same file */}
        <div><RingPieChart budgetId={budgetId} /></div> 
        <div className="span2"><LatestScans /></div>
      </div>
    </article>
  );
}

export default Home;