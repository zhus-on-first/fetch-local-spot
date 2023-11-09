// src/components/auth/ResetPasswordPage.js
import React, { useState } from 'react';
import { useAuthInfo } from '@propelauth/react';


import "../styles/auth.css";
import { useHistory } from "react-router-dom";

function ResetPasswordPage() {
  const [email, setEmail] = useState('');
  const { sendPasswordResetEmail } = useAuthInfo ();
  const [error, setError] = useState("");

  const history = useHistory();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await sendPasswordResetEmail(email);
      history.push("/");
    } catch (error) {
      setError("Unable to send password reset email. Please try again.");
      console.error('Password reset request failed:', error);
    }
  };

  return (
    <div>
      <h2>Reset Password</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Email:
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <button type="submit">Send Reset Email</button>
      </form>
    </div>
  );
}

export default ResetPasswordPage;
