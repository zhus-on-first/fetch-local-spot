import React from 'react';
import { withAuthInfo, useRedirectFunctions, useLogoutFunction } from '@propelauth/react';

// Local imports
import Header from '../layout/Header';

function UserProfile({ isLoggedIn, user }) {
  const {redirectToLoginPage, redirectToSignupPage, redirectToAccountPage} = useRedirectFunctions()
  const logoutFunction = useLogoutFunction()

  if (isLoggedIn) {
      return (
        <div>
          <Header />
          <span>
            <h2>User Info</h2>
            {user && user.pictureUrl && <img src={user.pictureUrl} className="pictureUrl" alt="profile pic" />}
            <pre>user: {JSON.stringify(user, null, 2)}</pre>
          </span>
          <button onClick={redirectToAccountPage}>Account</button>
          <button onClick={logoutFunction }>Logout</button>
        </div>
      )
  } else {
      return (
        <div>
          <p>You are not logged in</p>
          <button onClick={redirectToLoginPage}>Login</button>
          <button onClick={redirectToSignupPage}>Signup</button>
        </div>
      )
  }
}

export default withAuthInfo(UserProfile);
