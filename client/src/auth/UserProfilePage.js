import React from 'react';
import { useAuthInfo, useRedirectFunctions } from '@propelauth/react';

function UserProfile() {
  const authInfo = useAuthInfo();
  const { redirectToLoginPage } = useRedirectFunctions();

  const handleLogin = () => {
    redirectToLoginPage();
  };

  if (authInfo.loading) {
    return <div>Loading...</div>;
  } else if (authInfo.isLoggedIn) {
    return <div>Email: {authInfo.user.email}</div>;
  } else {
    return (
      <div>
        You are not logged in.
        <button onClick={handleLogin}>Click here to login.</button> 
      </div>
    );
  }
}

export default UserProfile;
