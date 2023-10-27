import React from "react";


function LocationCard({ location }) {
    console.log("Location object:", location);
    
    // Render each location feature's name from strings array
    const featureNamesList = location.location_feature_names 
    ? location.location_feature_names.map((lfn) => {
        return <li key={lfn.id}>{lfn.location_feature_name}</li>;
        }) : "No location features available";
    
    // Render each reported features' name from array of strings
    const reportedFeaturesList = location.reported_features_names
    ? location.reported_features_names.map((rfn) => {
        return <li key={rfn.id}>{rfn.reported_feature_name}</li>;
        }) : "No reported features available";
        
    return (
        <div>
            <h3>Location ID {location.id}: {location.name}</h3>
            <p>{location.address}</p>
            <p>{location.phone}</p>
            <p>Location Type: {location.location_type_name}</p>
            <p>Location Features:</p>
            <ul>{featureNamesList}</ul>
            <p>Reported Features:</p>
            <ul>{reportedFeaturesList}</ul>
        </div>
    );
}


export default LocationCard;