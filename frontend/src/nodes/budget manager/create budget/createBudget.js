// import React, { useState } from 'react';
// import DatePicker from 'react-datepicker';
// import 'react-datepicker/dist/react-datepicker.css';
// import { NavLink } from 'react-router-dom';

// const CreateBudget = () => {

//     const [selectedValue, setSelectedValue] = useState();
//     const [totalAmount, setTotalAmount] = useState();
//     const [startDate, setStartDate] = useState(null);
//     const [endDate, setEndDate] = useState(null);

   
//     const createBudgetUrl = 'http://127.0.0.1:5000/api/v1/budget/create';
//     const categoryData = "http://127.0.0.1:5000/api/v1/category/";

//     const categories = [];

//     fetch(categoryData, {
//         method: 'GET',
//         headers: {'Content-Type': 'application/json', },
//         credentials: 'include'
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('Server response was not ok');
//         }
//         return response.json(); 
//     })
//     .then(data => {
//         console.log('Success:', data);
//         categories = data;
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });

//     /*
//     try{
//         if(categoryData){
//             console.log(categoryData.message);
//             for(const category in categoryData.data){
//                 categories.push(category.category_name);
//             }
//         }
//     }
//     catch(e){
//         console.log(`Cannot get categories, error: ${e}`);
//     };*/
  
//     const handleDropdownChange = (event) => {
//       setSelectedValue(event.target.value);
//     };
//     const getTotalAmount = (event) => {
//         setTotalAmount(event.target.value);
//     };
//     const handleStartDateChange = (date) => {
//         setStartDate(date);
//     };
    
//     const handleEndDateChange = (date) => {
//         setEndDate(date);
//     };
//     const formatDateToString = (date) => {
//         return date ? date.toISOString().split('T')[0] : ''; 
//       };

//     function getBudget(){

//         const startDateString = formatDateToString(startDate);
//         const endDateString = formatDateToString(endDate);

//         const data = {
//             category_id: selectedValue,
//             total_amount: totalAmount,
//             start_date: startDateString,
//             end_date: endDateString
//         }
//      console.log(data);
//      return data;
//     }

//     function CreateBudget(){
//         fetch(createBudgetUrl, {
//             method: 'POST',
//             headers: {'Content-Type': 'application/json', },
//             body: JSON.stringify(getBudget()),
//             credentials: 'include'
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Server response was not ok');
                
//             }
//             return response.json(); 
//         })
//         .then(data => {
//             console.log('Success:', data); 
//             window.location.href ="/budget-managing";
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });


//     }


//     return(
//         <article>
//             <h1>Create Budget</h1>
//             <div>
//                 <div>
//                     <label>Category: </label>
//                     <select id="categories" value={selectedValue} onChange={handleDropdownChange} required>4
//                     <option selected disabled>Select category</option>
//                     {categories.map((category, index) => (
//                     <option key={index} value={index}>
//                         {category}
//                     </option>
//                     ))}
//                     </select>
//                 </div>
//                 <div>
//                     <label>Total amount: </label>

//                     <input type="number" placeholder="budget amount" value={totalAmount} onChange={getTotalAmount}></input>
//                 </div>
//                 <div>
//                     <label>Start Date: </label>
//                     <DatePicker
//                         selected={startDate}
//                         onChange={handleStartDateChange}
//                         selectsStart
//                         startDate={startDate}
//                         endDate={endDate}
//                         placeholderText="Select start date"
//                     />
//                     <br />
//                     <label>End Date: </label>
//                     <DatePicker
//                         selected={endDate}
//                         onChange={handleEndDateChange}
//                         selectsEnd
//                         startDate={startDate}
//                         endDate={endDate}
//                         minDate={startDate}
//                         placeholderText="Select end date"
//                     />
//                     </div>
//             </div>
//             <button><NavLink to="/budget-managing">Cancel</NavLink></button>
//             <button onClick={CreateBudget}>Create budget</button>
//         </article>


//     )
// }

// export default CreateBudget;

import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import { NavLink } from 'react-router-dom';
import 'react-datepicker/dist/react-datepicker.css';
import './../general.css';

const CreateBudget = () => {
    const [selectedValue, setSelectedValue] = useState('');
    const [totalAmount, setTotalAmount] = useState('');
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);
    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(false);

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
        return <div>Loading...</div>;
    }

    return (
        <article>
            <h1>Create Budget</h1>
            <div>
                <div>
                    <label>Category: </label>
                    <select value={selectedValue} onChange={handleDropdownChange} required>
                        <option value="" disabled>Select category</option>
                        {categories.map((category) => (
                            <option key={category.category_id} value={category.category_id}>
                                {category.category_name}
                            </option>
                        ))}
                    </select>
                </div>
                <div>
                    <label>Total amount: </label>
                    <input type="number" placeholder="Budget amount" value={totalAmount} onChange={handleTotalAmountChange} />
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
                <div>
                    <button><NavLink to="/budget-managing">Cancel</NavLink></button>
                    <button onClick={createBudget}>Create Budget</button>
                </div>
            </div>
        </article>
    );
}

export default CreateBudget;
