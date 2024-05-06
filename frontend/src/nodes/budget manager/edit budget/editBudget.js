import React, { useEffect, useState } from 'react';
import { useParams, NavLink } from 'react-router-dom';
import 'react-datepicker/dist/react-datepicker.css';

const EditPage = () => {
  const { id } = useParams();
  const [item, setItem] = useState(null);
  const [selectedValue, setSelectedValue] = useState();
  const [totalAmount, setTotalAmount] = useState();
  const [startDate, setStartDate] = useState();
  const [endDate, setEndDate] = useState();
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBudget = async () => {
      try {
        const budgetByIdUrl = `http://127.0.0.1:5000/api/v1/budget/${id}`;
        const response = await fetch(budgetByIdUrl, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include'
        });

        if (!response.ok) {
          throw new Error('Failed to fetch budget');
        }

        const data = await response.json();
        console.log(data);
        setItem(data.data);
        setSelectedValue(data.data.category_id);
        setTotalAmount(data.data.total_amount);
        setStartDate(data.data.start_date);
        setEndDate(data.data.end_date);
      } catch (error) {
        console.error('Error fetching budget:', error);
        setError('Cannot fetch data for the specified budget ID');
      } finally {
        setLoading(false);
      }
    };

    const fetchCategories = async () => {
      try {
        const categoryDataUrl = 'http://127.0.0.1:5000/api/v1/category/';
        const response = await fetch(categoryDataUrl, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include'
        });

        if (!response.ok) {
          throw new Error('Failed to fetch categories');
        }

        const data = await response.json();
        console.log(data.message);
        setCategories(data.data);
      } catch (error) {
        console.error('Cannot get categories, error:', error);
      }
    };

    fetchBudget();
    fetchCategories();
  }, [id]);

  const getTotalAmount = (event) => {
    setTotalAmount(event.target.value);
  };

  const updateBudget = async () => {
    try {
      const budgetByIdUrl = `http://127.0.0.1:5000/api/v1/budget/${id}`;
      const response = await fetch(budgetByIdUrl, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ total_amount: totalAmount }),
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error('Failed to update budget');
      }

      const data = await response.json();
      console.log('Success:', data);
      alert("Updated your budget successfully!")
    } catch (error) {
      console.error('Error updating budget:', error);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <article>
      <h1>Edit Budget</h1>
      {!item ? (
        <p>Cannot fetch data for budget ID {id}</p>
      ) : (
        <>
          <div>
            <div>
              <label>Category: </label>
              <p>{categories.find(category => category.category_id === selectedValue)?.category_name}</p>
            </div>
            <div>
              <label>Total Amount: </label>
              <input
                type="number"
                placeholder="Budget amount"
                value={totalAmount}
                onChange={getTotalAmount}
              />
            </div>
            <div>
              <label>Start Date: </label>
              <p>{startDate}</p>
              <br />
              <label>End Date: </label>
              <p>{endDate}</p>
            </div>
          </div>
          <button>
            <NavLink to="/budget-managing">Cancel</NavLink>
          </button>
          <button onClick={updateBudget}>Update Budget</button>
        </>
      )}
    </article>
  );
};

export default EditPage;