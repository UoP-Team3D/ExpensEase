import React, { useEffect, useState } from 'react';
import { Link } from "react-router-dom";

export default function Home() {
    const [message, setMessage] = useState('');

    useEffect(() => {
      fetch('http://localhost:5000/api/hello') //test backend connection
        .then(response => response.json())
        .then(data => setMessage(data.message));
    }, []);
  
    return (
      <div>
        <p>Message from backend: {message}</p>
      </div>
    );
    }