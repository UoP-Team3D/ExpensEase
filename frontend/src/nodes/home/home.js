import React from 'react';
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
    <>
      <svg width="200" height="200" viewBox="0 0 200 200">
        {budgets.map((budget, index) => {
          const dashArray = (budget.percentage / 100) * circumference;
          // Calculate the stroke dashoffset for the current segment
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
      <div style={{ textAlign: 'center', marginTop: '10px' }}>
        You have £{remainingBudget}/£{totalBudget} budget left
      </div>
    </>
  );
};

const LatestScans = () => {
  // Dummy data for the table rows
  const scanData = [
    { dateTime: '12/04/2024 14:22', location: 'Location A', amount: '£150' },
    { dateTime: '11/04/2024 09:15', location: 'Location B', amount: '£75' },
    { dateTime: '10/04/2024 16:45', location: 'Location C', amount: '£200' },
    // ... add more scan entries as needed
  ];

  return (
    <div className="latest-scans-container">
      <div className="latest-scans-header">Latest Scans:</div>
      <div className="latest-scans-table">
        <div className="table-header">
          <span>DATE/TIME</span>
          <span>WHERE?</span>
          <span>AMOUNT</span>
        </div>
        {scanData.map((scan, index) => (
          <div className="table-row" key={index}>
            <span>{scan.dateTime}</span>
            <span>{scan.location}</span>
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
        <div className="span2"><LatestScans /></div> {/* Latest Scans Table */}
        {/* <div>3</div>
        <div className="span2">4</div>
        <div>5</div>
        <div>6</div>
        <div>7</div>
        <div>8</div>
        <div>9</div>
        <div>10</div>
        <div>11</div>
        <div>12</div>
        <div>13</div>
        <div>14</div>
        <div>15</div>
        <div>16</div> */}
      </div>
    </article>
  );
}

export default Home;