import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { withRequiredAuthInfo } from '@propelauth/react';


function PrivateRoute({ component: Component, ...rest }) {
  const ComponentWithAuth = withRequiredAuthInfo(Component, {
    displayWhileLoading: <div>Loading...</div>,
    displayIfLoggedOut: <Redirect to="/login" />
  });

  return <Route {...rest} render={(props) => <ComponentWithAuth {...props} />} />;
}

export default PrivateRoute;
