import React, { useState, useEffect } from "react";

const Scan = () => {
    const [file, setFile] = useState(null);
    const [imagePreviewUrl, setImagePreviewUrl] = useState("");
    const [uploadStatus, setUploadStatus] = useState("");
    const [showConfirmation, setShowConfirmation] = useState(false);
    const [editMode, setEditMode] = useState(false);
    const [receiptData, setReceiptData] = useState({});
    const [editedTotalPrice, setEditedTotalPrice] = useState("");
    const [editedCategory, setEditedCategory] = useState("");
    const [categories, setCategories] = useState([]);

    useEffect(() => {
        fetchCategories();
    }, []);

    const fetchCategories = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/category/', {
                method: 'GET',
                credentials: 'include'
            });
            if (!response.ok) {
                throw new Error('Failed to fetch categories');
            }
            const data = await response.json();
            setCategories(data.data);
        } catch (error) {
            console.error('Fetch categories error:', error);
        }
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagePreviewUrl(reader.result);
            };
            reader.readAsDataURL(file);
            setFile(file);
        }
    };

    const handleSubmit = async () => {
        if (!file) {
            alert("Please select a file first!");
            return;
        }
    
        const formData = new FormData();
        formData.append('receipt_image', file);
    
        setUploadStatus("Uploading...");
        try {
            const uploadResponse = await fetch('http://127.0.0.1:5000/api/v1/receipt/upload', {
                method: 'POST',
                body: formData,
                credentials: 'include'  // Include credentials for cross-origin requests
            });
    
            if (!uploadResponse.ok) {
                throw new Error(`HTTP error! status: ${uploadResponse.status}`);
            }
    
            const data = await uploadResponse.json();
    
            setUploadStatus("Upload successful!");
            setReceiptData(data.data);
            setEditedTotalPrice(data.data.total_price);
            setEditedCategory(data.data.category);
            setShowConfirmation(true);
        } catch (error) {
            setUploadStatus(`Upload failed: ${error.message}`);
            console.error("Error in fetching:", error);
        }
    };

    const handleConfirm = async () => {
        const { receipt_id } = receiptData;
        const saveReceiptBody = JSON.stringify({
            receipt_id: receipt_id,
            description: "Received from Scan",
            total_price: editedTotalPrice,
            category: editedCategory
        });

        try {
            const saveResponse = await fetch('http://127.0.0.1:5000/api/v1/receipt/save_receipt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',  // Include credentials for cross-origin requests
                body: saveReceiptBody
            });

            if (saveResponse.ok) {
                setShowConfirmation(false);
                setEditMode(false);
                alert('Receipt saved successfully!');
                setImagePreviewUrl('');
            } else {
                throw new Error('Failed to save receipt');
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    };

    const handleEdit = () => {
        setEditMode(true);
    };

    const handleCancelEdit = () => {
        setEditMode(false);
        setEditedTotalPrice(receiptData.total_price);
        setEditedCategory(receiptData.category);
    };

    return (
        <article>
            <h1>Scan your receipts:</h1>
            <div>
                <h2>Add Image:</h2>
                <input
                    type="file"
                    accept="image/*"
                    capture="camera"
                    onChange={handleFileChange}
                />
                <button onClick={handleSubmit}>Submit</button>
                {imagePreviewUrl && (
                    <div>
                        <h3>Preview:</h3>
                        <img src={imagePreviewUrl} alt="Preview" style={{ maxWidth: '50%' }} />
                    </div>
                )}
                {uploadStatus && <p>{uploadStatus}</p>}
                {showConfirmation && (
                    <div>
                        <h3>Does the receipt's details look accurate?</h3>
                        <p>Category: {receiptData.category}, Total Price: £{receiptData.total_price}</p>
                        <button onClick={handleConfirm}>Yes</button>
                        <button onClick={handleEdit}>No</button>
                    </div>
                )}
                {editMode && (
                    <div>
                        <h3>Edit Receipt Details:</h3>
                        <label>Total Price:</label>
                        <input type="text" value={editedTotalPrice} onChange={e => setEditedTotalPrice(e.target.value)} />
                        <label>Category:</label>
                        <select value={editedCategory} onChange={e => setEditedCategory(e.target.value)}>
                            {categories.map(category => (
                                <option key={category.category_id} value={category.category_name}>{category.category_name}</option>
                            ))}
                        </select>
                        <button onClick={handleConfirm}>Save Changes</button>
                        <button onClick={handleCancelEdit}>Cancel</button>
                    </div>
                )}
            </div>
        </article>
    );
};

export default Scan;
