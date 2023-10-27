import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom/";

// Local imports
import Header from "../components/Header";
import LocationCard from "../components/LocationCard";
import ReportsByLocationId from "../components/ReportsByLocationId";
import Footer from "../components/Footer";


function LocationDetailsPage() {
  const { id } = useParams()
  const [isLoading, setIsLoading] = useState(false);
  const [locationDetails, setLocationDetails] = useState({});
  const [reportsDetails, setReportsDetails] = useState([]);
  const [errors, setErrors] = useState([]);

  // const id = 1;

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);

      // Fetch location details by location id
      const locationResponse = await fetch(`/locations/${id}`);
      console.log("Fetching location data...");
      if (locationResponse.ok) {
        const data = await locationResponse.json();
        console.log("Location data received:", data);
        if (data) {
          setLocationDetails(data);
        }
      } else {
        const errorMessages = await locationResponse.json();
        setErrors(errorMessages.errors);
      }

      // Fetch reports by location id
        const reportsResponses = await fetch(`/reports/location/${id}`);
        console.log("Fetching report by location data...");
        if (reportsResponses.ok) {
          const data = await reportsResponses.json();
          console.log("Reports data received:", data);
          setReportsDetails(data);
        } else {
          const errorMessages = await reportsResponses.json();
          console.group("Error received:", errorMessages);
          setErrors(errorMessages.errors);
        }

      setIsLoading(false);
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
          <LocationCard location={locationDetails} />
          <div>
          <h2>Reports for this location</h2>
          <ReportsByLocationId reports={reportsDetails} />
          </div>
          <Footer />
          {errors.map((err) => (
            <p key={err} style={{ color: "red" }}>
              {err}
            </p>
          ))}
        </>
      )}
    </div>
  );
}

export default LocationDetailsPage;
