import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";


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
        <Route path="/locations/find-a-hike">
          <FindHikePage />
        </Route>
        <Route path="/locations/find-a-ride">
          <FindRidePage />
        </Route>
        <Route path="/locations/find-a-food-spot">
          <FindFoodPage />
        </Route>
        <Route path="/locations/:id">
          <LocationDetailsPage />
        </Route>
        <Route>
          {/* Catch all page. Test with http://localhost:3000/locations//page/1 */}
          <NotFoundPage />
        </Route>

      </Switch>
    </Router>
  );
}

export default App;
