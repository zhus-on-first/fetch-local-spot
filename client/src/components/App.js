import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";

import LocationList from "./LocationList"; 

function App() {

  return (
    <div className="App">
      <h1>Fetch! Local Spots</h1>
      <h2>Sniff.Sit.Stay.Visit.</h2>
      
      <LocationList />

    </div>
  );
}

export default App;
