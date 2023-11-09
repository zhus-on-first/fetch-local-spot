import React from "react";
import { useHistory } from "react-router-dom";

import { useRedirectFunctions } from '@propelauth/react';
import { useLogoutFunction } from '@propelauth/react';

import "../styles/NavBurger.css"

function NavBurger(){
    const history = useHistory();

    const { redirectToLoginPage } = useRedirectFunctions();
    const { redirectToSignupPage } = useRedirectFunctions();
    const logout = useLogoutFunction();

    const handleLogin = () => {
    // redirectToLoginPage({ postLoginRedirectUrl: 'http://yourapp.com/home' });
    redirectToLoginPage();
    };

    const handleRegister = () => {
        redirectToSignupPage();
    }
    const handleProfile = () => {
        history.push('/profile');
    }

    const handleLogout = () => {
        logout(true);
    };

    return (
        <div className="navburger-container">
        <button onClick={handleLogin}>Login</button>
        <button onClick={handleRegister}>Register</button>
        <button onClick={handleProfile}>My Profile</button>
        <button onClick={handleLogout}>Logout</button>
        </div>
    )
}


export default NavBurger;