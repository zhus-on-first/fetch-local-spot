import React from 'react';
import { useAuthInfo, useRedirectFunctions } from '@propelauth/react';

// Local imports
import Header from '../layout/Header';

function UserProfile() {
  const authInfo = useAuthInfo();
  const { redirectToLoginPage, redirectToSignupPage, redirectToAccountPage } = useRedirectFunctions();

  const handleLogin = () => {
    redirectToLoginPage({ postLoginRedirectUrl: "http://localhost:3000/profile" });
  };

  if (authInfo.loading) {
    return (
      <div>
        <Header />
        <div>Loading...</div>
      </div>
    );
  } else if (authInfo.isLoggedIn) {
    return (
      <div>
        <Header />
        <div>Email: {authInfo.user.email}</div>
      </div>
    );
  } else {
    return (
      <div>
        <Header />
        <div>
          You are not logged in.
          <button onClick={handleLogin}>Click here to login.</button> 
        </div>
      </div>
    );
  }
}

export default UserProfile;
