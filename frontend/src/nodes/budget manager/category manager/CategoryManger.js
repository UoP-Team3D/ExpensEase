import React, { useState, useEffect } from 'react';
import { FiInfo } from 'react-icons/fi';
import '../CatMan.css';

const CatMan = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingCategoryId, setEditingCategoryId] = useState(null);
  const [newCategory, setNewCategory] = useState('');
  const [editName, setEditName] = useState('');
  const [visibleDescriptions, setVisibleDescriptions] = useState({});

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
      fetchCategories();
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
      fetchCategories();
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
      fetchCategories();
      setNewCategory('');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const isProtectedCategory = (categoryName) => {
    const protectedCategories = ['Groceries', 'Eating Out', 'Personal Upkeep'];
    return protectedCategories.includes(categoryName);
  };

  const getCategoryDescription = (categoryName) => {
    const descriptions = {
      'Groceries': 'Expenses related to buying food and household items from grocery stores or supermarkets.',
      'Eating Out': 'Expenses incurred while dining at restaurants, cafes, or other food establishments.',
      'Personal Upkeep': 'Expenses related to personal care, clothing, and maintenance.',
    };
    return descriptions[categoryName] || '';
  };

  const showDescription = (categoryName) => {
    setVisibleDescriptions((prevState) => ({
      ...prevState,
      [categoryName]: true,
    }));
  };

  const hideDescription = (categoryName) => {
    setTimeout(() => {
      setVisibleDescriptions((prevState) => ({
        ...prevState,
        [categoryName]: false,
      }));
    }, 200);
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
                  <div className="category-info">
                    <div className="category-name-wrapper">
                      <span className="category-name">{category.category_name}</span>
                      {isProtectedCategory(category.category_name) && (
                        <FiInfo
                          className="info-icon"
                          onMouseEnter={() => showDescription(category.category_name)}
                          onMouseLeave={() => hideDescription(category.category_name)}
                        />
                      )}
                    </div>
                    {visibleDescriptions[category.category_name] && (
                      <div className="category-description">
                        {getCategoryDescription(category.category_name)}
                      </div>
                    )}
                    {!isProtectedCategory(category.category_name) && (
                      <div className="category-actions">
                        <button onClick={() => {
                          setEditingCategoryId(category.category_id);
                          setEditName(category.category_name);
                        }} className="catman-button edit-button">Edit</button>
                        <button onClick={() => deleteCategoryById(category.category_id)} className="catman-button delete-button">Delete</button>
                      </div>
                    )}
                  </div>
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