import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import 'react-datepicker/dist/react-datepicker.css';
import { NavLink } from 'react-router-dom';

const EditPage = () => {
    const { id } = useParams();
    const [item, setItem] = useState(null);
    const [selectedValue, setSelectedValue] = useState();
    const [totalAmount, setTotalAmount] = useState();
    const [startDate, setStartDate] = useState();
    const [endDate, setEndDate] = useState(); 

    useEffect(() => {
        const budgetByIdUrl = `https://127.0.0.1:5000/api/v1/budget/${id}`;
        fetch(budgetByIdUrl, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            },
            credentials: 'include'
          })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                setItem(data);
                setSelectedValue(data.category_name);
                setTotalAmount(data.total_amount);
                setStartDate(data.start_date);
                setEndDate(data.end_date);
            })
            .catch(error => console.error('ERROR fetching Item:', error));
        },[id]);

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
    
    if(item){
        setSelectedValue(categories[item.category_id]);
        setTotalAmount(item.total_amount);
        setStartDate(item.start_date);
        setEndDate(item.end_date); 
    } else{
        console.error('Cannot get data.')
    }
   
    const getTotalAmount = (event) => {
        setTotalAmount(event.target.value);
    };

    function updateBudget(){
        const budgetByIdUrl = `https://127.0.0.1:5000/api/v1/budget/${id}`;
        fetch(budgetByIdUrl, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json',},
            body: JSON.stringify({total_amount: totalAmount}),
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
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }



    return (
        <article>
            <h1>Edit budget</h1>
            {!item? <p>Cannot fetch data for budget id {id}</p>
            :
            <>
            <div>
                <div>
                    
                    <label>Category: </label>
                    <p>{selectedValue}</p>
                </div>
                <div>
                    <label>Total amount: </label>

                    <input type="number" placeholder="budget amount" value={totalAmount} onChange={getTotalAmount}></input>
                </div>
                <div>
                    <label>Start Date: </label>
                    <p>{startDate}</p>
                    <br />
                    <label>End Date: </label>
                    <p>{endDate}</p>
                    </div>
            </div>
            <button><NavLink to="/budget-managing">Cancel</NavLink></button>
            <button onClick={updateBudget}>Update budget</button>
            </>
            }
        </article>
    );
};

export default EditPage;