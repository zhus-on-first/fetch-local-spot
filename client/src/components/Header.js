import React, { useContext } from "react"
import { Link } from "react-router-dom"
import { ThemeContext } from "../ThemeContext"

function Header() {
    const { theme, setTheme } = useContext(ThemeContext);

    const handleToggle = () => {
        console.log("Current theme:", theme);  // Log current theme
        setTheme(theme === "light" ? "dark" : "light");
    }

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
            <div>
                {/* <button onClick={() => setTheme(theme === "light" ? "dark" : "light")}> */}
                <button onClick={handleToggle}>
                    Toggle Theme
                </button>
            </div>

            <div className="navburger-container">
                <button>☰</button>
            </div>
        </header>
    )
}

export default Header;