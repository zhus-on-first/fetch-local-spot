import React from "react";

import "./index.css";
import App from "./components/App";
import { ThemeProvider } from "./ThemeContext";
import { createRoot } from "react-dom/client";

import { AuthProvider } from "@propelauth/react";

const container = document.getElementById("root");
const root = createRoot(container);

root.render(
    <AuthProvider authUrl={process.env.REACT_APP_AUTH_URL}>
        <ThemeProvider>
            <App />
        </ThemeProvider>
    </AuthProvider>
);
