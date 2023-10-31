import React from "react";

import Header from "../components/Header";
import HorizontalFilter from "../components/HorizontalFilter";
import LocationList from "../components/LocationList";

function HomePage() {


  return (
    <div>
        <Header />
        <HorizontalFilter />
        <h3>All Locations:</h3>
        <LocationList />
    </div>
  );
};

export default HomePage;
