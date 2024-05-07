import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import { NavLink } from 'react-router-dom';
import 'react-datepicker/dist/react-datepicker.css';
import { Pie } from 'react-chartjs-2';
import { Chart, ArcElement, Title, Tooltip, Legend } from 'chart.js';
import '../CreateBudget.css';

Chart.register(ArcElement, Title, Tooltip, Legend);

const CreateBudget = () => {
  const [selectedValue, setSelectedValue] = useState('');
  const [totalAmount, setTotalAmount] = useState('');
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const fetchCategories = async () => {
      setLoading(true);
      const categoryDataUrl = 'http://127.0.0.1:5000/api/v1/category/';
      try {
        const response = await fetch(categoryDataUrl, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include'
        });
        if (!response.ok) {
          throw new Error('Failed to fetch categories');
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

  useEffect(() => {
    const fetchBudget = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/budget/${selectedValue}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include'
        });
        if (!response.ok) {
          throw new Error('Failed to fetch budget');
        }
        const result = await response.json();
        const budget = result.data;
        const usedAmount = budget.total_amount - budget.current_amount;
        const remainingAmount = budget.current_amount;
        setChartData({
          labels: [`Used (${usedAmount})`, `Remaining (${remainingAmount})`],
          datasets: [
            {
              data: [usedAmount, remainingAmount],
              backgroundColor: ['#FF6384', '#36A2EB']
            }
          ]
        });
      } catch (error) {
        console.error('Error:', error);
      }
    };

    if (selectedValue) {
      fetchBudget();
    }
  }, [selectedValue]);

  const handleDropdownChange = (event) => {
    setSelectedValue(event.target.value);
  };

  const handleTotalAmountChange = (event) => {
    setTotalAmount(event.target.value);
  };

  const handleStartDateChange = (date) => {
    setStartDate(date);
  };

  const handleEndDateChange = (date) => {
    setEndDate(date);
  };

  const formatDateToString = (date) => {
    return date ? date.toISOString().split('T')[0] : '';
  };

  const createBudget = async () => {
    const data = {
      category_id: selectedValue,
      total_amount: totalAmount,
      start_date: formatDateToString(startDate),
      end_date: formatDateToString(endDate)
    };

    try {
      const createBudgetUrl = 'http://127.0.0.1:5000/api/v1/budget/create';
      const response = await fetch(createBudgetUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        credentials: 'include'
      });
      if (!response.ok) {
        throw new Error('Failed to create budget');
      }
      const result = await response.json();
      console.log('Success:', result);
      window.location.href = "/budget-managing"; // Redirect on success
    } catch (error) {
      console.error('Error:', error);
    }
  };

  if (loading) {
    return (
      <article className="create-container">
        <section className="create-header">
          <h1>Create Budget</h1>
        </section>
        <section className="loading">
          <p>Loading...</p>
        </section>
      </article>
    );
  }

  return (
    <article className="create-container">
      <section className="create-header">
        <h1>Create Budget</h1>
      </section>
      <section className="create-form">
        <div className="form-group">
          <label>Category:</label>
          <select value={selectedValue} onChange={handleDropdownChange} required className="form-select">
            <option value="" disabled>Select category</option>
            {categories.map((category) => (
              <option key={category.category_id} value={category.category_id}>
                {category.category_name}
              </option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label>Total amount:</label>
          <input type="number" placeholder="Budget amount" value={totalAmount} onChange={handleTotalAmountChange} className="form-input" />
        </div>
        <div className="form-group">
          <label>Start Date:</label>
          <DatePicker
            selected={startDate}
            onChange={handleStartDateChange}
            selectsStart
            startDate={startDate}
            endDate={endDate}
            placeholderText="Select start date"
            className="form-datepicker"
          />
        </div>
        <div className="form-group">
          <label>End Date:</label>
          <DatePicker
            selected={endDate}
            onChange={handleEndDateChange}
            selectsEnd
            startDate={startDate}
            endDate={endDate}
            minDate={startDate}
            placeholderText="Select end date"
            className="form-datepicker"
          />
        </div>
      </section>
      <section className="create-actions">
        <button className="create-button cancel-button">
          <NavLink to="/budget-managing">Cancel</NavLink>
        </button>
        <button className="create-button submit-button" onClick={createBudget}>Create Budget</button>
      </section>
      {chartData && (
        <section className="budget-overview">
          <h2>Budget Overview</h2>
          <div className="chart-container">
            <Pie
              data={chartData}
              options={{
                plugins: {
                  legend: {
                    position: 'bottom'
                  },
                  title: {
                    display: true,
                    text: `Budget Overview for Category ${selectedValue}`
                  }
                }
              }}
            />
          </div>
        </section>
      )}
    </article>
  );
};

export default CreateBudget;