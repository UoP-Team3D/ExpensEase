import React, { useState } from "react";

const Scan = () => {
    const [file, setFile] = useState(null);
    const [imagePreviewUrl, setImagePreviewUrl] = useState("");
    const [uploadStatus, setUploadStatus] = useState("");
    const [showConfirmation, setShowConfirmation] = useState(false);
    const [receiptData, setReceiptData] = useState({});

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
    
            const data = await uploadResponse.json(); // Assuming the response is JSON formatted.
    
            setUploadStatus("Upload successful!");
            setReceiptData(data.data);
            setShowConfirmation(true);
        } catch (error) {
            setUploadStatus(`Upload failed: ${error.message}`);
            console.error("Error in fetching:", error);
        }
    };

    const handleConfirm = async () => {
        const { receipt_id, total_price, category } = receiptData;
        const saveReceiptBody = JSON.stringify({
            receipt_id: receipt_id,
            description: "Received from Scan",
            total_price: total_price,
            category: category
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
                alert('Receipt saved successfully!');
                setImagePreviewUrl('');
            } else {
                throw new Error('Failed to save receipt');
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
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
                        <p>Category: {receiptData.category}, Total Price: ${receiptData.total_price}</p>
                        <button onClick={handleConfirm}>Yes</button>
                        <button onClick={() => setShowConfirmation(false)}>No</button>
                    </div>
                )}
            </div>
        </article>
    );
};

export default Scan;
