import React, { useContext, useState } from "react";
import { Link } from "react-router-dom";

// Local imports
import { ThemeContext } from "../styles/ThemeContext";
import NavBurger from "./NavBurger";
import "../styles/HeaderStyles.css"
import LogoImage from "../common/logo.png"

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
    <header className="header">
      <div className="header-logo">
        <Link to="/">
          {/* <h1>Fetch! Local Spots</h1>
          <h2>Sniff. Sit. Stay. Visit.</h2> */}
          <img src={LogoImage} alt="logo"></img>
        </Link>
      </div>
      <div className="header-search">
        <input type="text" placeholder="Search nothing. I ain't working."/>
      </div>
      <div className="header-profile">
        <button onClick={handleToggle} className="theme-toggle">
          Toggle Theme
        </button>
        {/* <button onClick={toggleNav} className="burger-button">
          <span className="burger-line"></span>
          <span className="burger-line"></span>
          <span className="burger-line"></span>
        </button> */}
        <button onClick={toggleNav}>☰</button>
        {showNav && <NavBurger />}
      </div>
    </header>
  )
}

export default Header;
