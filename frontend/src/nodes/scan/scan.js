import React, { useState, useEffect } from "react";
import "./Scan.css"; // Create a separate CSS file for styling

const Scan = () => {
  const [file, setFile] = useState(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState("");
  const [uploadStatus, setUploadStatus] = useState("");
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [receiptData, setReceiptData] = useState({});
  const [editedTotalPrice, setEditedTotalPrice] = useState("");
  const [editedCategory, setEditedCategory] = useState("");
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/v1/category/", {
        method: "GET",
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error("Failed to fetch categories");
      }
      const data = await response.json();
      setCategories(data.data);
    } catch (error) {
      console.error("Fetch categories error:", error);
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
    formData.append("receipt_image", file);

    setUploadStatus("Uploading...");
    try {
      const uploadResponse = await fetch(
        "http://127.0.0.1:5000/api/v1/receipt/upload",
        {
          method: "POST",
          body: formData,
          credentials: "include",
        }
      );

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
      category: editedCategory,
    });

    try {
      const saveResponse = await fetch(
        "http://127.0.0.1:5000/api/v1/receipt/save_receipt",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: saveReceiptBody,
        }
      );

      if (saveResponse.ok) {
        setShowConfirmation(false);
        alert("Receipt saved successfully!");
        setImagePreviewUrl("");
      } else {
        throw new Error("Failed to save receipt");
      }
    } catch (error) {
      alert(`Error: ${error.message}`);
    }
  };

  const handleCancel = () => {
    setShowConfirmation(false);
  };

  return (
    <article className="scan-container">
      <h1 className="scan-heading">Scan Your Receipts</h1>
      <div className="scan-section">
        <h2 className="scan-subheading">Add Image</h2>
        <div className="file-input-container">
          <input
            type="file"
            accept="image/*"
            capture="camera"
            onChange={handleFileChange}
            className="file-input"
          />
        </div>
        <button onClick={handleSubmit} className="scan-button submit-button">
          Submit
        </button>
        {imagePreviewUrl && (
          <div className="preview-container">
            <h3 className="preview-heading">Preview</h3>
            <img src={imagePreviewUrl} alt="Preview" className="preview-image" />
          </div>
        )}
        {uploadStatus && <p className="upload-status">{uploadStatus}</p>}
      </div>
      {showConfirmation && (
        <div className="confirmation-popup">
          <div className="confirmation-content">
            <h3 className="confirmation-heading">Confirm Receipt Details</h3>
            <p className="prediction-text">We've predicted the following...</p>
            <div className="receipt-details">
              <div className="detail-field">
                <label className="detail-label">Category:</label>
                <select
                  value={editedCategory}
                  onChange={(e) => setEditedCategory(e.target.value)}
                  className="detail-select"
                >
                  {categories.map((category) => (
                    <option
                      key={category.category_id}
                      value={category.category_name}
                    >
                      {category.category_name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="detail-field">
                <label className="detail-label">Total Price:</label>
                <div className="price-input">
                  <span className="price-symbol">£</span>
                  <input
                    type="text"
                    value={editedTotalPrice}
                    onChange={(e) => setEditedTotalPrice(e.target.value)}
                    className="price-input-field"
                  />
                </div>
              </div>
            </div>
            <div className="confirmation-buttons">
              <button
                onClick={handleConfirm}
                className="scan-button confirm-button"
              >
                Confirm
              </button>
              <button
                onClick={handleCancel}
                className="scan-button cancel-button"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </article>
  );
};

export default Scan;