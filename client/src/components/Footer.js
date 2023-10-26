import React from "react"
import { Link } from "react-router-dom"

function Footer() {
    return (
        <header>
            <div className="logo-container">
                <h1>Footer</h1>
                <h2>Sniff. Sit. Stay. Visit.</h2>
            </div>
            <div className="search-container">
                <input type="text" placeholder="Search"/>
            </div>
        </header>
    )
}

export default Footer;