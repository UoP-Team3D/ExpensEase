import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { NavLink } from 'react-router-dom';

const CreateBudget = () => {

    const [selectedValue, setSelectedValue] = useState();
    const [totalAmount, setTotalAmount] = useState();
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);

   
    const createBudgetUrl = 'http://127.0.0.1:5000/api/v1/budget/create';
    const categoryData = "http://127.0.0.1:5000/api/v1/category/";

    const categories = [];
    try{
        if(categoryData.success){
            console.log(categoryData.message);
            for(const category in categoryData.data){
                categories.push(category.category_name);
            }
        }
    }
    catch(e){
        console.log(`Cannot get categories, error: ${e}`);
    };
  
    const handleDropdownChange = (event) => {
      setSelectedValue(event.target.value);
    };
    const getTotalAmount = (event) => {
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
     return data;
    }

    function CreateBudget(){
        fetch(createBudgetUrl, {
            method: 'POST',
            headers: {'Content-Type': 'application/json', },
            body: JSON.stringify(getBudget()),
            credentials: 'include'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server response was not ok');
                
            }
            return response.json(); 
        })
        .then(data => {
            console.log('Success:', data); 
            window.location.href ="/budget-managing";
        })
        .catch(error => {
            console.error('Error:', error);
        });


    }


    return(
        <article>
            <h1>Create Budget</h1>
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

                    <input type="number" placeholder="budget amount" value={totalAmount} onChange={getTotalAmount}></input>
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
            <button><NavLink to="/budget-managing">Cancel</NavLink></button>
            <button onClick={CreateBudget}>Create budget</button>
        </article>


    )
}

export default CreateBudget;