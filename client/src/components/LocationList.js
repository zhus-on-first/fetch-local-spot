import React, { useEffect, useState } from "react";
import LocationCard from "./LocationCard";

function LocationList() {
    const locations = [
        {
            id: 1,
            name: "Central Park",
            address: "New York, New York",
            phone: "123-456-7890",
            location_type_id: 1
        },
        {
            id: 2,
            name: "Golden Gardens",
            address: "Seattle, WA",
            phone: "123-456-7890",
            location_type_id: 2
        }
    ]
    return (
        <div>
            {locations.map((location) => (
                <LocationCard key={location.id} location={location} />
            ))}
        </div>
    );
}

export default LocationList