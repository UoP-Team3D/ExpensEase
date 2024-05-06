import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import { FiCalendar, FiSearch } from 'react-icons/fi';
import 'react-datepicker/dist/react-datepicker.css';
import './History.css';

const History = () => {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showDateRange, setShowDateRange] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchLastExpenses();
  }, []);

  const fetchLastExpenses = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/expense/?sort_by=date&sort_order=desc&page=1&per_page=5', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error('Failed to fetch last expenses');
      }

      const json = await response.json();
      setExpenses(json.data);
    } catch (error) {
      console.error('Error fetching last expenses:', error);
      setError('An error occurred while fetching last expenses. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const fetchExpenses = async (start, end) => {
    if (!start || !end) {
      setError('Please select a valid date range.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/expense/?start_date=${formatDate(start)}&end_date=${formatDate(end)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error('Failed to fetch expenses');
      }

      const json = await response.json();
      setExpenses(json.data);
    } catch (error) {
      console.error('Error fetching expenses:', error);
      setError('An error occurred while fetching expenses. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (date) => {
    return [
      date.getFullYear(),
      ("0" + (date.getMonth() + 1)).slice(-2),
      ("0" + date.getDate()).slice(-2)
    ].join('-');
  };

  const handleDateChange = (dates) => {
    const [start, end] = dates;
    setStartDate(start);
    setEndDate(end);
    setShowDateRange(false);
    fetchExpenses(start, end);
  };

  const formatDisplayDate = (date) => {
    if (date) {
      return date.toLocaleDateString('en-GB', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      });
    }
    return '';
  };

  return (
    <article className="history-container">
      <h1 className="history-title">Receipts History</h1>
      <div className="search-container">
        <button
          type="button"
          onClick={() => setShowDateRange(!showDateRange)}
          className="date-range-btn"
        >
          <FiCalendar className="calendar-icon" />{' '}
          {startDate && endDate
            ? `${formatDisplayDate(startDate)} - ${formatDisplayDate(endDate)}`
            : 'Select Date Range'}
        </button>
        {showDateRange && (
          <div className="date-range-picker">
            <DatePicker
              selected={startDate}
              onChange={handleDateChange}
              startDate={startDate}
              endDate={endDate}
              selectsRange
              inline
            />
          </div>
        )}
        <button
          type="button"
          onClick={() => fetchExpenses(startDate, endDate)}
          className="search-btn"
          disabled={!startDate || !endDate}
        >
          <FiSearch className="search-icon" /> Search
        </button>
      </div>
      {loading ? (
        <div className="loading">Loading...</div>
      ) : error ? (
        <div className="error">{error}</div>
      ) : (
        <>
          {expenses.length === 0 ? (
            <div className="no-results">No receipts found.</div>
          ) : (
            <div className="receipts-table">
              <div className="table-header">
                <div className="header-cell">Date</div>
                <div className="header-cell">Category</div>
                <div className="header-cell">Amount</div>
              </div>
              {expenses.map((expense, index) => (
                <div key={index} className="table-row">
                  <div className="table-cell">{expense.date}</div>
                  <div className="table-cell">{expense.category}</div>
                  <div className="table-cell">£{expense.amount.toFixed(2)}</div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </article>
  );
};

export default History;