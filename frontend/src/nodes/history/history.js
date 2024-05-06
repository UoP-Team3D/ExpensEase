import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import { FiCalendar } from 'react-icons/fi';
import 'react-datepicker/dist/react-datepicker.css';
import './../general.css';

const History = () => {
    const [startDate, setStartDate] = useState(new Date());
    const [expenses, setExpenses] = useState([]);
    const [loading, setLoading] = useState(false);
    const [showDatePicker, setShowDatePicker] = useState(false);
    const [showManualEntry, setShowManualEntry] = useState(false);
    const [manualDate, setManualDate] = useState('');

    const handleManualDateChange = (event) => {
        const { value } = event.target;
        let formattedDate = value.replace(/[^\d]/g, ""); // Remove non-digit characters
    
        // Automatically add hyphens after DD and MM
        if (formattedDate.length > 4) {
            // Add hyphens for both day and month
            formattedDate = formattedDate.slice(0, 2) + '-' + formattedDate.slice(2, 4) + '-' + formattedDate.slice(4);
        } else if (formattedDate.length > 2) {
            // Add hyphen for day only
            formattedDate = formattedDate.slice(0, 2) + '-' + formattedDate.slice(2);
        }
    
        // Set the formatted date, ensuring it does not exceed the required length
        if (formattedDate.length <= 10) {
            setManualDate(formattedDate);
        }
    };
    
    
    const fetchExpenses = async (selectedDate) => {
        setLoading(true);
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/v1/expense/?start_date=${selectedDate}&end_date=${selectedDate}`,{
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
        } finally {
            setLoading(false);
        }
    };

    const handleDateChange = (date) => {
        const formattedDate = formatDate(date);
        setStartDate(date);
        setShowDatePicker(false);
        setShowManualEntry(false);
        fetchExpenses(formattedDate);
    };

    const formatDate = (date) => {
        return [
            ("0" + date.getDate()).slice(-2),
            ("0" + (date.getMonth() + 1)).slice(-2),
            date.getFullYear()
        ].join('-');
    };

    const confirmManualDate = () => {
        const parts = manualDate.split('-');
        if (parts.length === 3) {
            const date = new Date(parts[2], parts[1] - 1, parts[0]); // Convert DD-MM-YYYY to Date object
            if (!isNaN(date)) {
                setStartDate(date);
                setShowManualEntry(false);
                setShowDatePicker(false);
                fetchExpenses(manualDate); // Use the DD-MM-YYYY format for the API if required
            } else {
                alert('Please enter a valid date.');
            }
        }
    };

    return (
        <article className="history-container">
            <h1>Receipts History</h1>
            {loading ? (
                <div>Loading...</div>
            ) : (
                <div className="receipts-list">
                    {expenses.map((expense, index) => (
                        <div key={index} className="receipt-entry">
                            <div className="receipt-date">{expense.date}</div>
                            <div className="receipt-description">{expense.category}</div> {/* Changed from expense.description to expense.category */}
                            <div className="receipt-amount">£{expense.amount.toFixed(2)}</div>
                        </div>
                    ))}
                </div>
            )}
            <div className="button-and-date-picker-container">
                <button
                    type="button"
                    onClick={() => setShowDatePicker(!showDatePicker)}
                    className="choose-date-btn"
                    style={{ backgroundColor: 'darkorange', color: 'white' }}
                >
                    Choose Date
                </button>
                {showDatePicker && (
                    <DatePicker
                        selected={startDate}
                        onChange={handleDateChange}
                        inline
                        dateFormat="dd-MM-yyyy"
                    />
                )}
                <button
                    type="button"
                    onClick={() => setShowManualEntry(!showManualEntry)}
                    className="manual-entry-btn"
                >
                    <FiCalendar />
                </button>
                {showManualEntry && (
                    <div>
                        <input
                            className="manual-date-input"
                            type="text"
                            placeholder="DD-MM-YYYY"
                            value={manualDate}
                            onChange={handleManualDateChange}
                        />
                        <button
                            className="confirm-date-btn"
                            onClick={confirmManualDate}
                        >
                            Confirm
                        </button>
                    </div>
                )}
            </div>
        </article>
    );
}

export default History;
