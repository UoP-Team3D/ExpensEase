import React, { useEffect, useState } from 'react';
import './../grid.css';

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
        <div class="grid see-outline">
          <div>1</div>
          <div class="span2">2</div>
          <div>3</div>
          <div class="span2">4</div>
          <div>5</div>
          <div>6</div>
          <div>7</div>
          <div>8</div>
          <div>9</div>
          <div>10</div>
          <div>11</div>
          <div>12</div>
          <div>13</div>
          <div>14</div>
          <div>15</div>
          <div>16</div>
        </div>
      </article>
    );
}

export default Home;