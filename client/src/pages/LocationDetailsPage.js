import React, { useEffect, useState, useCallback } from "react";
import { useParams } from "react-router-dom";

// Local imports
import Header from "../components/Header";
import LocationCard from "../components/LocationCard";
import NewReportForm from "../components/NewReportForm";
import ReportsByLocationId from "../components/ReportsByLocationId";
import Footer from "../components/Footer";


function LocationDetailsPage() {
  const { id } = useParams()
  // const id = 1;

  // Location Details States
  const [isLoading, setIsLoading] = useState(false);
  const [locationDetails, setLocationDetails] = useState({});
  const [reportsDetails, setReportsDetails] = useState([]);
  const [errors, setErrors] = useState([]);

  const fetchData = useCallback(async () => {
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
        console.log("Error received:", errorMessages);
        setErrors(errorMessages.errors);
      }

    setIsLoading(false);
  }, [id]);
  
  useEffect(() => {
    fetchData();
  }, [fetchData]);


  // New Report Form State and Helper Functions
  const [isFormVisible, setIsFormVisible] = useState(false);

  const toggleForm = () => {
    setIsFormVisible(!isFormVisible);
  };

  const handleNewReport = (newReport) => {
    setReportsDetails(prevReports => [...prevReports, newReport])
  }

  const handleDeleteReport = async (reportId) => {
    try{
      console.log("Report Id for Deletion:", reportId)
      const response = await fetch(`/reports/${reportId}`, {
        method: "DELETE",
      });

      if (response.ok) {
        fetchData();
      } else {
        const errorMessages = await response.json();
        console.log("Delete failed:", errorMessages)
      }

    } catch (error) {
      console.log("An error occurred:", error)
    }
  }

  return (
    <div>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <>
          <Header />
          <h1>Location Details</h1>
          <LocationCard location={locationDetails} />

          <h2>Add A New Report</h2>
          {!isFormVisible && <button onClick={toggleForm}>Add Your Report</button>}
          {isFormVisible && <NewReportForm locationId={id} handleNewReport={handleNewReport} toggleForm={toggleForm} />}

          <div>
          <h2>Reports for this location</h2>
          <ReportsByLocationId reports={reportsDetails} onDeleteReport={handleDeleteReport} />
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
