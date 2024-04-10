import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const BudMan = () => {

    const mainBudget = "http://127.0.0.1:5000/api/v1/budget/1"

    
    
    const [selectedValue, setSelectedValue] = useState();
    const [totalAmount, setTotalAmount] = useState();
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);
  
    const handleDropdownChange = (event) => {
      setSelectedValue(event.target.value);
    }
    const getTotalAmount = (event) => {
        setTotalAmount(event.target.value);
    }

    const handleStartDateChange = (date) => {
        setStartDate(date);
    };
    
    const handleEndDateChange = (date) => {
        setEndDate(date);
    };
    const formatDateToString = (date) => {
        return date ? date.toISOString().split('T')[0] : ''; 
      };

    const categories = [
        'General budget',
        'Groceries',
        'Eating out',
        'Entertainment'
      ];

    function getBudget(){

        const startDateString = formatDateToString(startDate);
        const endDateString = formatDateToString(endDate);

        const data = {
            category_id: selectedValue,
            total_amount: totalAmount,
            start_date: startDateString,
            end_date: endDateString
        }

     console.log(data);
    }


    return(
        <article>
            <h1>Budget manager</h1>
            <div>
                <div>
                    <label>Category: </label>
                    <select id="categories" value={selectedValue} onChange={handleDropdownChange} required>4
                    <option selected disabled>Select category</option>
                    {categories.map((category, index) => (
                    <option key={index} value={index}>
                        {category}
                    </option>
                    ))}
                    </select>
                </div>
                <div>
                    <label>Total amount: </label>

                    <input type="number" placeholder="budget amount" value={totalAmount} onChange={getTotalAmount} required></input>
                </div>
                <div>
                    <label>Start Date: </label>
                    <DatePicker
                        selected={startDate}
                        onChange={handleStartDateChange}
                        selectsStart
                        startDate={startDate}
                        endDate={endDate}
                        placeholderText="Select start date"
                    />
                    <br />
                    <label>End Date: </label>
                    <DatePicker
                        selected={endDate}
                        onChange={handleEndDateChange}
                        selectsEnd
                        startDate={startDate}
                        endDate={endDate}
                        minDate={startDate}
                        placeholderText="Select end date"
                    />
                    </div>
            </div> 
            <button onClick={getBudget}>Create Budget</button>
        </article>


    )
}

export default BudMan;

