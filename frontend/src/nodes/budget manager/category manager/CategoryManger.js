import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';

const CatMan = () => {

    const categoryData = "http://127.0.0.1:5000/api/v1/category/";

    const [editingCategoryId, setEditingCategoryId] = useState(null);
    const [newCategory, setNewCategory] = useState(null);

    const categories = [    ];

    fetch(categoryData, {
        method: 'GET',
        headers: {'Content-Type': 'application/json', },
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
        categories = data;
    })
    .catch(error => {
        console.error('Error:', error);
    });
                
   

    const deleteCategoryById = (id) => {
        deleteCategory(id)
      };

    function deleteCategory(id) {
    fetch(categoryData+id, { 
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to delete category');
        }
        console.log('Category deleted successfully');
    })
    .catch(error => {
        console.error('Error:', error); 
    });
    }

    function updateCategory(id){
        fetch(categoryData+id, { 
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
        })
        .then(response => {
            if (!response.ok) {
                console.log('Failed to Update category');
                return false
            }
            console.log('Category updated successfully');
            return true
        })
        .catch(error => {
            console.error('Error:', error);
            return false
        });
    }
   

    const startEditing = (categoryId) => {
        setEditingCategoryId(categoryId);
    };

    const getCategoryId = (id) => {
        const update = updateCategory(id);
        if(update){
            console.log('Updated category:', categories[id]);
            setEditingCategoryId(null);
        }
        
    };

    const cancelEdit = () => {
        setEditingCategoryId(null);
    };

    function createNewCategory(){
        fetch(categoryData, { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
        })
        .then(response => {
            if (!response.ok) {
                console.log('Failed to create category');
                return false
            }
            console.log('Category created successfully');
            return true
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    const inputChange = (event) => {
        setNewCategory(event.target.value);
    };
    

    return(
        <article>
            <section>
                <div>
                    <h4>Create new category:</h4>
                    <p>Add a new category so you can have better control over where you spend your money.</p>
                    <input type="text" placeholder='new category name' value={newCategory} onChange={inputChange} /><br/>
                    <button onClick={createNewCategory}>Create new category</button>
                </div>
                <h1>List of your categories:</h1>
                {categories.length? <ul>
                    {Object.values(categories).map((item) => (
                        <li key={item.category_id}>
                            {editingCategoryId === item.category_id ? (
                                <>
                                    <input 
                                        type="text" 
                                        value={item.category_name}  
                                    />
                                    <button onClick={() => getCategoryId(item.category_id)}>Update</button>
                                    <button onClick={cancelEdit}>Cancel</button>
                                </>
                            ) : (
                                <>
                                    <span>Category name: {item.category_name}</span><br />
                                    <button onClick={() => startEditing(item.category_id)}>Edit</button>
                                    <button onClick={() => deleteCategoryById(item.category_id)}>Delete</button>
                                </>
                            )}
                        </li>
                    ))}
                </ul>:
                <em>Cannot get categories</em>
                }
            </section>
        </article>
        /*<article>
                <section>
                    
                    <h1>List of your budgets:</h1>
                    <ul>
                        {Object.values(categories).map((item, ) => (
                                <li key={index} id={item.category_id}>
                                    <span>Category name: {item.category_name}</span><br/>
                                    
                                    <button>
                                    <NavLink to={`/edit/${index}`}>Edit</NavLink>
                                    </button>
                                    <button id={item.category_id} onClick={deleteCategoryById}>Delete</button>
                                </li>
                            ))}
                    </ul>
                </section>
            
        </article>

                            */
    )
}

export default CatMan;

