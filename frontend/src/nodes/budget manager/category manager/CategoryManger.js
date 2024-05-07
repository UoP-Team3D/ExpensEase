import React, { useState, useEffect } from 'react';
import '../CatMan.css'; // Create a separate CSS file for styling

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
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
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

  const isProtectedCategory = (categoryName) => {
    const protectedCategories = ['Groceries', 'Eating Out', 'Personal Upkeep'];
    return protectedCategories.includes(categoryName);
  };

  return (
    <article className="catman-container">
      <section className="catman-header">
        <h1>Manage Your Categories</h1>
      </section>
      {loading ? (
        <p>Loading categories...</p>
      ) : (
        <section className="category-list">
          {categories.map(category => (
            <div key={category.category_id} className="category-item">
              <div className="category-details">
                {editingCategoryId === category.category_id ? (
                  <>
                    <input
                      type="text"
                      value={editName}
                      onChange={e => setEditName(e.target.value)}
                      className="category-edit-input"
                    />
                    <div className="category-actions">
                      <button onClick={() => updateCategory(category.category_id)} className="catman-button save-button">Save</button>
                      <button onClick={() => setEditingCategoryId(null)} className="catman-button cancel-button">Cancel</button>
                    </div>
                  </>
                ) : (
                  <>
                    <span className="category-name">{category.category_name}</span>
                    {!isProtectedCategory(category.category_name) && (
                      <div className="category-actions">
                        <button onClick={() => {
                          setEditingCategoryId(category.category_id);
                          setEditName(category.category_name);
                        }} className="catman-button edit-button">Edit</button>
                        <button onClick={() => deleteCategoryById(category.category_id)} className="catman-button delete-button">Delete</button>
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          ))}
        </section>
      )}
      <section className="create-category">
        <h4>Create New Category:</h4>
        <div className="create-category-input">
          <input
            type="text"
            placeholder="New category name"
            value={newCategory}
            onChange={(e) => setNewCategory(e.target.value)}
          />
          <button onClick={createNewCategory} className="catman-button create-button">Create</button>
        </div>
      </section>
    </article>
  );
};

export default CatMan;