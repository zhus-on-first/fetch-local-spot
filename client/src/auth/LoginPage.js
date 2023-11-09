import React from 'react';
import { useRedirectFunctions } from '@propelauth/react';

function LoginPage() {
  const { redirectToLoginPage } = useRedirectFunctions();

  const handleLogin = () => {
    // redirectToLoginPage({ postLoginRedirectUrl: 'http://yourapp.com/home' });
    redirectToLoginPage();
  };

  return (
    <div>
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default LoginPage;
