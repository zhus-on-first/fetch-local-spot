import React from "react";


function LocationCard({ location }) {
    console.log("Location object:", location);
    
    const featureNamesList = location.location_feature_names.map((location_feature_name, index) => {
        return <li key={index}>{location_feature_name}</li>;
    });

    const reportedFeaturesList = location.reported_features_names.map((reported_features_name, index) => {
        return <li key={index}>{reported_features_name}</li>;
    });
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