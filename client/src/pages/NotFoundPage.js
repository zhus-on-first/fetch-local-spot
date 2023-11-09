import React from "react";
import { Link, useLocation } from "react-router-dom";
import Search from "../components/Search";
import Footer from "../layout/Footer";

function NotFoundPage() {
    const location = useLocation();

    return (

        <div>
            <h1>Oops! You tried to visit "{location.pathname}".</h1>
            <p>But it might have been moved, deleted, or perhaps never existed.</p>
            <img src="404_image.jpg" alt="Page not found" />
            <div>
                <Link to="/">Return to Home</Link>
            </div>
            <p>Or use this search bar:</p><Search />
            <Footer />
        </div>
    );
}

export default NotFoundPage;
