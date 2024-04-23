import React from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate for redirection
import './../grid.css';

const RingPieChart = ({ totalBudget, remainingBudget }) => {
  const radius = 70; // Radius of the circle
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
              strokeWidth="40" // This controls the thickness of the ring
              strokeDasharray={`${dashArray} ${circumference - dashArray}`}
              strokeDashoffset={dashOffset}
              transform="rotate(-90 100 100)"
            />
          );
        })}
      </svg>
      <div className="budget-text">
        You have £{remainingBudget}/£{totalBudget} budget left
      </div>
    </div>
  );
};


const LatestScans = () => {
  const scanData = [
    { dateTime: '12/04/2024 14:22', location: 'Location A', amount: '£150' },
    { dateTime: '11/04/2024 09:15', location: 'Location B', amount: '£75' },
    { dateTime: '10/04/2024 16:45', location: 'Location C', amount: '£200' },
  ];

  return (
    <div className="latest-scans-container">
      <div className="latest-scans-header">Latest Scans:</div>
      <div className="latest-scans-table">
      <div className="table-header">
        <span>DATE/TIME</span>
        <span className="where-column">WHERE?</span>
        <span>AMOUNT</span>
      </div>
      {scanData.map((scan, index) => (
        <div className="table-row" key={index}>
          <span>{scan.dateTime}</span>
          <span className="where-column">{scan.location}</span>
          <span>{scan.amount}</span>
        </div>
       ))}
      </div>
    </div>
  );
};

const Home = () => {

  return (
    <article>
      <div className="grid see-outline">
        <div><RingPieChart totalBudget={1000} remainingBudget={650} /></div>
        <div className="span2"><LatestScans /></div>
      </div>
    </article>
  );
}

export default Home;
