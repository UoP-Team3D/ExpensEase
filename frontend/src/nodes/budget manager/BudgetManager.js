import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';

const BudMan = () => {

    const url = true;

    const dummyData =[{
                    budget_id: 0,
                    user_id: 0,
                    category_id: 0,
                    total_amount: 6547,
                    current_amount: 2000,
                    start_date: "2024-05-01",
                    end_date: "2024-05-07"
                    
                },]
    let budgets;
                
    const getBudgetsUrl = 'http://127.0.0.1:5000/api/v1/budget/';

    fetch(getBudgetsUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        budgets = data.data
    })
    .catch(error => {
        console.error('Error fetching the data:', error);
    });

    return(
        <article>
            {url? (
                <section>
                    <h1>List of your budgets:</h1>
                    <ul>
                        {Object.values(dummyData).map((item, index) => (
                                <li key={index}>
                                    <span>Total amount: £{item.total_amount}3</span><br/>
                                    <span>Start date: {item.start_date}</span><br/>
                                    <span>End date: {item.end_date}</span><br/>
                                    <button onClick={console.log("test")}>Edit</button>
                                    <button>Delete</button>
                                </li>
                            ))}
                    </ul>
                </section>
            ):(
            <h1>Create your first budget-plan</h1>

            )}
            <button><NavLink to="/create-budget">Create new budget</NavLink></button>
        </article>


    )
}

export default BudMan;

