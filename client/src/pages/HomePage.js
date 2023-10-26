import React from "react";

import Header from "../components/Header";
import HorizontalFilter from "../components/HorizontalFilter";
import LocationList from "../components/LocationList";
import NewReportForm from "../components/NewReportForm";

function HomePage() {


  return (
    <div>
        <Header />
        <HorizontalFilter />
        <NewReportForm />
        <h3>All Locations:</h3>
        <LocationList />
    </div>
  );
};

export default HomePage;
