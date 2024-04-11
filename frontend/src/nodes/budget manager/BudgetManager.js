import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';

const BudMan = () => {

    const url = true;

    const dummyData = {
                    bud1:{
                    category_id: 0,
                    total_amount: 6547,
                    start_date: "2024-05-01",
                    end_date: "2024-05-07"
                    },
                };

    return(
        <article>
            {url? (
                <section>
                    <h1>List of your budgets:</h1>
                    <ul>
                        {Object.values(dummyData).map((item, index) => (
                                <li key={index}>
                                    <span>Category: {item.category_id}</span><br/>
                                    <span>Total amount: £{item.total_amount}3</span><br/>
                                    <span>Start date: {item.start_date}</span><br/>
                                    <span>End date: {item.end_date}</span>
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

