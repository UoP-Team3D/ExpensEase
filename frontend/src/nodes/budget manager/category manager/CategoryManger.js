import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';

const CatMan = () => {
    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [editingCategoryId, setEditingCategoryId] = useState(null);
    const [newCategory, setNewCategory] = useState('');
    const [editName, setEditName] = useState('');

    const fetchCategories = async () => {
        const categoryData = "http://127.0.0.1:5000/api/v1/category/";
        try {
            const response = await fetch(categoryData, {
                method: 'GET',
                headers: {'Content-Type': 'application/json'},
                credentials: 'include'
            });
            const json = await response.json();
            if (response.ok) {
                setCategories(json.data);
            } else {
                throw new Error(json.message || 'Failed to fetch categories');
            }
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCategories();
    }, []);

    const deleteCategoryById = async (id) => {
        const categoryData = `http://127.0.0.1:5000/api/v1/category/${id}`;
        try {
            const response = await fetch(categoryData, {
                method: 'DELETE',
                headers: {'Content-Type': 'application/json'},
                credentials: 'include',
            });
            if (!response.ok) {
                throw new Error('Failed to delete category');
            }
            fetchCategories(); // Refresh categories after deletion
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const updateCategory = async (id) => {
        if (!editName.trim()) {
            alert('Category name cannot be empty.');
            return;
        }
        const categoryData = `http://127.0.0.1:5000/api/v1/category/${id}`;
        const data = { category_name: editName };
        try {
            const response = await fetch(categoryData, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data),
                credentials: 'include',
            });
            if (!response.ok) {
                throw new Error('Failed to update category');
            }
            fetchCategories(); // Refresh categories after update
            setEditingCategoryId(null);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const createNewCategory = async () => {
        if (!newCategory.trim()) {
            alert('Category name cannot be empty.');
            return;
        }
        const categoryData = `http://127.0.0.1:5000/api/v1/category/`;
        const data = { category_name: newCategory };
        try {
            const response = await fetch(categoryData, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data),
                credentials: 'include',
            });
            if (!response.ok) {
                throw new Error('Failed to create category');
            }
            fetchCategories(); // Refresh categories after creation
            setNewCategory('');
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <article>
            <section>
                <h1>Manage Your Categories</h1>
                {loading ? (
                    <p>Loading categories...</p>
                ) : (
                    <ul>
                        {categories.map(category => (
                            <li key={category.category_id}>
                                {editingCategoryId === category.category_id ? (
                                    <>
                                        <input
                                            type="text"
                                            value={editName}
                                            onChange={e => setEditName(e.target.value)}
                                        />
                                        <button onClick={() => updateCategory(category.category_id)}>Save</button>
                                        <button onClick={() => setEditingCategoryId(null)}>Cancel</button>
                                        </>
                            ) : (
                                <>
                                    <span>{category.category_name}</span>
                                    <button onClick={() => {
                                        setEditingCategoryId(category.category_id);
                                        setEditName(category.category_name);
                                    }}>Edit</button>
                                    <button onClick={() => deleteCategoryById(category.category_id)}>Delete</button>
                                </>
                            )}
                        </li>
                    ))}
                </ul>
            )}
            <div>
                <h4>Create new category:</h4>
                <input
                    type="text"
                    placeholder="New category name"
                    value={newCategory}
                    onChange={(e) => setNewCategory(e.target.value)}
                />
                <button onClick={createNewCategory}>Create</button>
            </div>
        </section>
    </article>
);
}

export default CatMan;