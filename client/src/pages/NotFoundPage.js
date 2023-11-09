import React from "react";
import { Link, useLocation } from "react-router-dom";

// Local imports
import Search from "../components/Search";
import Footer from "../layout/Footer";
import NotFoundImage from "../common/404.jpg"

function NotFoundPage() {
    const location = useLocation();

    return (

        <div>
            <h1>Oops! You tried to visit "{location.pathname}".</h1>
            <p>But it might have been moved, deleted, or perhaps never existed.</p>
            <div>
                <Link to="/">Return to Home</Link>
            </div>
            <p>Or use this search bar:</p><Search />
            <img src={NotFoundImage} alt="Page not found" />

            <Footer />
        </div>
    );
}

export default NotFoundPage;
