import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import { FiCalendar } from 'react-icons/fi'; // Importing calendar icon from react-icons
import 'react-datepicker/dist/react-datepicker.css';
import './../grid.css';

const History = () => {
    const [startDate, setStartDate] = useState(new Date());
    const [showDatePicker, setShowDatePicker] = useState(false); // State to manage DatePicker visibility
    const [showManualEntry, setShowManualEntry] = useState(false); // State to manage manual entry visibility
    const [manualDate, setManualDate] = useState(''); // State to hold the manually entered date

    // Dummy data for receipts
    const receipts = [
        { date: '5/10/2023', description: "McDonald's meal (eating out)", amount: '-£14.72' },
        { date: '5/10/2023', description: 'Costa Coffee (eating out)', amount: '-£3.50' },
        { date: '5/10/2023', description: 'Gym membership (entertainment)', amount: '-£22.50' },
        { date: '4/10/2023', description: 'Lidl shop (groceries)', amount: '-£80.00' },
        { date: '4/10/2023', description: 'Car insurance (personal upkeep)', amount: '-£500.00' },
        // ... more data
    ];

    const toggleDatePicker = () => {
        setShowDatePicker(!showDatePicker); // Toggle the visibility of the DatePicker
    };

    const handleDateChange = (date) => {
        setStartDate(date);
        setShowManualEntry(false); // Hide manual entry if date is selected from the calendar
        setShowDatePicker(false); // Also hide the date picker
    };

    const confirmManualDate = () => {
        const date = new Date(manualDate);
        // Validate the date before setting it
        if (!isNaN(date)) {
            setStartDate(date);
            setShowManualEntry(false); // Hide manual entry form
            setShowDatePicker(false); // Also hide the date picker
        } else {
            alert('Please enter a valid date.');
        }
    };

    return (
        <article className="history-container">
            <h1>Receipts History</h1>
            <div className="receipts-list">
                {receipts.map((receipt, index) => (
                    <div key={index} className="receipt-entry">
                        <div className="receipt-date">{receipt.date}</div>
                        <div className="receipt-description">{receipt.description}</div>
                        <div className="receipt-amount">{receipt.amount}</div>
                    </div>
                ))}
            </div>
            <div className="button-and-date-picker-container">
                <button
                    type="button"
                    onClick={toggleDatePicker}
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
                            placeholder="YYYY-MM-DD"
                            value={manualDate}
                            onChange={(e) => setManualDate(e.target.value)}
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