import React from "react";


function LocationCard({ location }) {
    console.log("Location object:", location);
    
    const featureNamesList = location.feature_names.map((feature_name, index) => {
        return <li key={index}>{feature_name}</li>;
    });
    return (
        <div>
            <h3>Location ID {location.id}: {location.name}</h3>
            <p>{location.address}</p>
            <p>{location.phone}</p>
            <p>Location Type: {location.location_type_name}</p>
            <p>Features:</p>
            <ul>{featureNamesList}</ul>
        </div>
    );
}


export default LocationCard;