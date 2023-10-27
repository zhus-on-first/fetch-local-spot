import React, { useEffect, useState } from "react";
import Header from "../components/Header";
import ReportCard from "../components/ReportCard";
import LocationCard from "../components/LocationCard";
import Footer from "../components/Footer";

function LocationDetailsPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [locationDetails, setLocationDetails] = useState({});
  const [reportDetails, setReportDetails] = useState([]);
  const [errors, setErrors] = useState([]);

  const id = 1;

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      console.log("Fetching data...");

      // Fetch location details by location id
      const locationResponse = await fetch(`/locations/${id}`);
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
        const reportResponse = await fetch(`/reports/location/${id}`);
        if (reportResponse.ok) {
          const data = await reportResponse.json();
          console.log("Reports data received:", data);
          setReportDetails(data);
        } else {
          const errorMessages = await reportResponse.json();
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
          <h2>Reports</h2>
          <ReportCard report={reportDetails} />
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
