import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";


import HomePage from "../pages/HomePage";
import LocationDetailsPage from "../pages/LocationDetailsPage"


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
        <Route path="/locations/1">
          <LocationDetailsPage />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
