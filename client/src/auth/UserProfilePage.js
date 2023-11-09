import React from 'react';
import { withAuthInfo, useRedirectFunctions, useLogoutFunction } from '@propelauth/react';

// Local imports
import Header from '../layout/Header';

function UserProfile(props) {
  const {redirectToLoginPage, redirectToSignupPage, redirectToAccountPage} = useRedirectFunctions()
  const logoutFunction = useLogoutFunction()

  if (props.isLoggedIn) {
      return (
        <div>
          <Header />
          <p>You are logged in as {props.user.email}</p>
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
