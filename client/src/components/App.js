// Standard imports
import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";


// PropelAuth
import LoginPage from "../auth/LoginPage";
import RegisterPage from "../auth/RegisterPage";
import UserProfile from "../auth/UserProfilePage";
import PrivateRoute from "../auth/PrivateRoute"


// Local imports
import HomePage from "../pages/HomePage";
import FindHikePage from "../pages/FindHikePage";
import FindRidePage from "../pages/FindRidePage";
import FindFoodPage from "../pages/FindFoodPage";
import LocationDetailsPage from "../pages/LocationDetailsPage";
import NotFoundPage from "../pages/NotFoundPage";


function App() {

  // if (isLoading) {
  //   return <div>Loading...</div>;
  // }

  return (
    <Router>
      <Switch>
        <Route path="/" exact>
          <HomePage />
        </Route>
        <Route path="/login" exact>
          <LoginPage />
        </Route>
        <Route path="/register" exact>
          <RegisterPage />
        </Route>
        <Route path="/profile" exact>
          <UserProfile />
        </Route>
        <PrivateRoute path="/locations/find-a-hike" component={FindHikePage} />
        <PrivateRoute path="/locations/find-a-ride" component={FindRidePage} />
        <PrivateRoute path="/locations/find-a-food-spot" component={FindFoodPage}/>
        <Route path="/locations/:id">
          <LocationDetailsPage />
        </Route>
        <Route>
          <NotFoundPage />
        </Route>

      </Switch>
    </Router>
  );
}

export default App;
