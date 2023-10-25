import React, { useEffect, useState } from 'react';
import LocationCard from "./LocationCard";

function FindHike() {
    const [locations, setLocations] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("http://127.0.0.1:5555/locations/find-a-hike");
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                const api_data = await response.json();
                setLocations(api_data);
            } catch (error) {
                console.error("There was a problem with the fetch:", error)
            }
        };
        fetchData();
    }, []); 

  console.log(locations);
  return (
    <div>

        {locations.map((location) => (
        <LocationCard key={location.id} location={location} />
      ))}
    </div>
  );
}

export default FindHike;
