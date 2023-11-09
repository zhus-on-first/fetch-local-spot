// src/components/auth/RegisterPage.js
import React, { useState } from 'react';
import { useAuthInfo } from '@propelauth/react';


import "../styles/auth.css";
import { useHistory } from "react-router-dom";

function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState("");
  const { register } = useAuthInfo ();
  
  const history = useHistory();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await register(email, password);
      history.push("/");
    } catch (error) {
      setError("Unable to register. Please check your details and try again.")
      console.error('Registration failed:', error);
    }
  };

  return (
    <div>
      <h2>Register</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Email:
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Password:
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default RegisterPage;
