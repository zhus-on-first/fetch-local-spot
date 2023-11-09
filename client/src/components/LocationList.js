import React, { useEffect, useState } from "react";
import LocationCard from "./LocationCard";

import "../styles/LocationCardStyles.css"

function LocationList() {
    const [locations, setLocations] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("/locations");
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                const apiData = await response.json();
                console.log(apiData)
                setLocations(apiData);
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
            )}
        </div>
    );
}

export default LocationList;