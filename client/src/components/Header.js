import React from "react"

function Header() {
    return (
        <header>
            <div className="logo-container">
                <h1>Fetch! Local Spots</h1>
                <h2>Sniff. Sit. Stay. Visit.</h2>
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