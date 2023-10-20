import React, {useState} from "react";

import Header from "../components/Header";
import LocationList from "../components/LocationList";
import HorizontalFilter from "../components/HorizontalFilter";
import LocationForm from "../components/LocationForm";

function HomePage() {
  const [successMessage, setSuccessMessage] = useState([])
    
  const handleNewLocation = (newLocation) => {
    setSuccessMessage("New location added successfully!");
  };


  return (
    <div>
        <Header />
        <HorizontalFilter />
        <h3>All Locations:</h3>
        <LocationList />
        <p>{successMessage}</p>
        <LocationForm handleNewLocation={handleNewLocation} />
    </div>
  );
}

export default HomePage;
