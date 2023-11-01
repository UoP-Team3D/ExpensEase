import React from 'react';
import { Link } from "react-router-dom";

export default function Home() {
    return(
    <article>
        <Link to="/scan">Scan</Link>
        <h1>This is the first page shown after login</h1>
    </article>
    )



}