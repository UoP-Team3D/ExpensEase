import React, { useState } from "react";

const Scan = () => {

    const [image, setImage] = useState(null);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onload = (event) => {
        setImage(event.target.result);
        };

        reader.readAsDataURL(file);
    };

    return(
        <article>
            <h1> Scan your recipts:</h1>
            <div>
            <h2>Add Image: </h2>
            <input
                type="file"
                accept="image/*"
                capture="camera" 
                onChange={handleFileChange}/>
            
            <button>Submit</button>
            {image && (
                <div>
                <h3>Preview:</h3>
                <img src={image} alt="Preview" style={{ maxWidth: '50%' }} />
                </div>
            )}
            </div>
        </article>
    )
}

export default Scan;