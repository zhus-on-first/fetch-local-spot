import React, { useContext, useState } from "react";
import { Link } from "react-router-dom";

// Local imports
import { ThemeContext } from "../styles/ThemeContext";
import NavBurger from "./NavBurger";
import "../styles/Header.css"

function Header() {
  const { theme, setTheme } = useContext(ThemeContext);
  const [showNav, setShowNav] = useState(false);

  const handleToggle = () => {
    console.log("Current theme:", theme);  // Log current theme
    setTheme(theme === "light" ? "dark" : "light");
  }

  const toggleNav = () => {
    setShowNav(!showNav);
  }

  return (
    <header>
      <div className="logo-container" >
        <Link to="/"><h1>Fetch! Local Spots</h1>
        <h2>Sniff. Sit. Stay. Visit.</h2>
        </Link>
      </div>
      <div className="search-container">
        <input type="text" placeholder="Search nothing. I ain't working."/>
      </div>
      <div>
        <button onClick={handleToggle}>
          Toggle Theme
        </button>
      </div>

      <div className="navburger-container">
        <button onClick={toggleNav}>☰</button>
        {showNav && <NavBurger />}
      </div>
    </header>
  )
}

export default Header;
