import React, { useState } from "react";

const Scan = () => {
    const [file, setFile] = useState(null);
    const [imagePreviewUrl, setImagePreviewUrl] = useState("");
    const [uploadStatus, setUploadStatus] = useState("");

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
            // Upload the receipt
            const uploadResponse = await fetch('http://127.0.0.1:5000/api/v1/receipt/upload', {
                method: 'POST',
                body: formData,
            });
            const uploadData = await uploadResponse.json();

            if (!uploadResponse.ok) {
                throw new Error(uploadData.message || "Upload failed");
            }

            // Save the receipt with additional data
            setUploadStatus("Saving receipt...");
            const saveResponse = await fetch('http://127.0.0.1:5000/api/v1/receipt/save_receipt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    receipt_id: uploadData.data.receipt_id,
                    description: "Received from Scan", // Static description, replace as needed
                    total_price: uploadData.data.total_price, // Assuming total_price is returned from upload
                    category: "General" // Static category, replace as needed
                })
            });
            const saveData = await saveResponse.json();

            if (!saveResponse.ok) {
                throw new Error(saveData.message || "Save failed");
            }

            setUploadStatus("Receipt processed and saved successfully!");
        } catch (error) {
            setUploadStatus(`Error: ${error.message}`);
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
            </div>
        </article>
    );
};

export default Scan;
