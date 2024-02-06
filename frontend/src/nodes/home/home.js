import React, { useEffect, useState } from 'react';

const Home = () => {
   
    
   const [jsonData,setData] = useState({});
    useEffect(() => {
      fetch('http://localhost:5000/api/hello')
      .then(response => {
        return response.json()
      })
      .then((data) => {
        console.log(data)
        setData(data);
      })
    },[]);

    return (
      <article>
        <p>Message from backend: {jsonData.message}</p>
      </article>
    );
}

export default Home;