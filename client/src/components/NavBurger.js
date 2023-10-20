import React from "react"
import { Link } from "react-router-dom"

function NavBurger(){
    return (
        <div style={{ display: 'none' }}>
        <Link to="/login">Login</Link>
        <Link to="/signup">Sign Up</Link>
        </div>
    )
}


export default NavBurger;