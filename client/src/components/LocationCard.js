import React, { useEffect, useState } from "react";

function LocationCard({ location }) {
    return (
        <div>
            <h3>{location.name}</h3>
            <p>{location.address}</p>
            <p>{location.phone}</p>
            <p>{location.location_type_id}</p>
        </div>
    );
}


export default LocationCard