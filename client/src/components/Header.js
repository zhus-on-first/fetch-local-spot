import React from "react"
import { Link } from "react-router-dom"

function Header() {
    return (
        <header>
            <div className="logo-container" >
                <Link to="/"><h1>Fetch! Local Spots</h1>
                <h2>Sniff. Sit. Stay. Visit.</h2>
                </Link>
            </div>
            <div className="search-container">
                <input type="text" placeholder="Search"/>
            </div>
            <div className="navburger-container">
                <button>☰</button>
            </div>
        </header>
    )
}

export default Header;