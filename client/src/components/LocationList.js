import React, { useEffect, useState } from "react";
import LocationCard from "./LocationCard";

function LocationList() {
    const [locations, setLocations] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("http://127.0.0.1:5555/locations");
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                const api_data = await response.json();
                console.log(api_data)
                setLocations(api_data);
            } catch (error) {
                console.error("There was a problem with the fetch:", error)
            }
        };
        fetchData();
    }, []); // empty array makes sure effect runs only once when it mounts.

    return (
        <div>
            {/* {locations.map((location) => (
                <LocationCard key={location.id} location={location} />
            ))} */}

            {locations.map((location) => {
                console.log("Current location:", location);
                return (
                <LocationCard 
                key={location.id} 
                location={location} 
                />)
            }
            )})
        </div>
    );
}

export default LocationList;