import React, { useEffect, useState } from "react";
import Header from "../components/Header"
import LocationCard from "../components/LocationCard";


function LocationDetailsPage() {
  const [isLoading, setIsLoading] = useState(false)
  const [locationDetails, setLocationDetails] = useState({});
  const [errors, setErrors] = useState([])
  
  const id = 1;

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true)
      console.log("Fetching data...")
      const response = await fetch(`/locations/${id}`);
        if (response.ok) {
          const data = await response.json();
          console.log("Data received:", data)
          if (data) { // Check that data is available before setting state
            setLocationDetails(data);
          }

        } else {
          const errorMessages = await response.json();
          console.group("Error received:", errorMessages)
          setErrors(errorMessages.errors)
        }
      setIsLoading(false)
    };
    fetchData();
  }, [id]);

    
  return (
      <div>
        {isLoading ? (
          <p>Loading...</p>
        ) : (
          <>
            <Header />
            <h1>Location Details</h1>
            <LocationCard location={locationDetails}/>
            {errors.map((err) => (
              <p key={err} style={{ color: "red" }}>
                {err}
              </p>
            ))}
          </>
        )}
      </div>
  );

};


export default LocationDetailsPage;