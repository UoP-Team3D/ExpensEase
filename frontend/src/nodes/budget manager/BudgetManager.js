import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';

const BudMan = () => {
    /*
    const dataBudgets =[{
                    budget_id: 0,
                    user_id: 0,
                    category_id: 0,
                    total_amount: 6547,
                    current_amount: 2000,
                    start_date: "2024-05-01",
                    end_date: "2024-05-07"   
                },];*/

    let budgets;
                
    const getBudgetsUrl = 'http://127.0.0.1:5000/api/v1/budget/';
    const deleteBudgetUrl ='http://127.0.0.1:5000/api/v1/budget/';

    const deleteBudgetByIndex = (id) => {
        deleteBudget(id);
      };

    function deleteBudget(id){
        fetch(deleteBudgetUrl+id, {
            method: 'DELETE',
            headers: {'Content-Type': 'application/json', },
            credentials: 'include',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server response was not ok');
            }
            console.log("deleted budget")
        })
        .catch(error => {
            console.error('Error:', error); 
        });
    }


    fetch(getBudgetsUrl,{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      })
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
            {dataBudgets? (
                <section>
                    <button><NavLink to="/create-budget">Create new budget</NavLink></button>
                    <button><NavLink to="/category-managing">Manage your categories</NavLink></button>
                    <h1>List of your budgets:</h1>
                    <ul>
                        {Object.values(budgets).map((item, index) => (
                                <li key={index} id={index}>
                                    <span>Total amount: £{item.total_amount}3</span><br/>
                                    <span>Start date: {item.start_date}</span><br/>
                                    <span>End date: {item.end_date}</span><br/>
                                    <button>
                                    <NavLink to={`/edit/${index}`}>Edit</NavLink>
                                    </button>
                                    <button  onClick={deleteBudgetByIndex(index)}>Delete</button>
                                </li>
                            ))}
                    </ul>
                </section>
            ):(
            <h1>Create your first budget-plan</h1>

            )}
        </article>


    )
}

export default BudMan;

