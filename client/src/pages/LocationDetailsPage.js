import React, { useEffect, useState, useCallback } from "react";
import { useParams } from "react-router-dom";

// PropelAuth
import { useAuthInfo, useRedirectFunctions } from "@propelauth/react";

// Local imports
import Header from "../layout/Header";
import LocationCard from "../components/LocationCard";
import NewReportForm from "../components/NewReportForm";
import ReportsByLocationId from "../components/ReportsByLocationId";
import Footer from "../layout/Footer";


function LocationDetailsPage() {
  const { id } = useParams()

  // PropelAuth
  const authInfo = useAuthInfo();
  const { redirectToLoginPage } = useRedirectFunctions();
  //PropelAuth redirect if not logged in
  // useEffect(() => {
  //   if (authInfo.loading) return;
  //   if (!authInfo.isLoggedIn) redirectToLoginPage();
  // }, [authInfo, redirectToLoginPage]);

  // Location Details States
  const [isLoading, setIsLoading] = useState(false);
  const [locationDetails, setLocationDetails] = useState({});
  const [reportsDetails, setReportsDetails] = useState([]);
  const [errors, setErrors] = useState([]);


  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setErrors([]);
    try {
      // Fetch location details by location id
      const locationResponse = await fetch(`/locations/${id}`);
      console.log("Fetching location data...");
      if (!locationResponse.ok) {
        const errorMessages = await locationResponse.json();
        setErrors((prevErrors) => [...prevErrors, ...errorMessages.errors]);
      }
      const data = await locationResponse.json();
      console.log("Location data received:", data);
      setLocationDetails(data);
  
      // Fetch reports by location id
      const reportsResponses = await fetch(`/reports/location/${id}`);
      console.log("Fetching report by location data...");
      if (!reportsResponses.ok) {
        const errorMessages = await reportsResponses.json();
        setErrors((prevErrors) => [...prevErrors, ...errorMessages.errors]);
      }
      const reportsData = await reportsResponses.json();
      console.log("Reports data received:", reportsData);
      setReportsDetails(reportsData);
    } catch (error) {
      // Handle network errors or other exceptions
      setErrors((prevErrors) => [...prevErrors, `An unexpected error occurred: ${error.message}`]);
    } finally {
      setIsLoading(false);
    }
  }, [id]);
  
  useEffect(() => {
    fetchData();
  }, [fetchData]);
  
  console.log("Reports details before passing to component:", reportsDetails);


  // Add a Report
  const [isFormVisible, setIsFormVisible] = useState(false);

  const toggleNewReportForm = () => {
    setIsFormVisible(!isFormVisible);
  };

  // const handleNewReport = (newReport) => {
  //   setReportsDetails(prevReports => [...prevReports, newReport])
  // }

  const refreshReports = async () => {
    try {
      const refreshReportsResponse = await fetch(`/reports/location/${id}`);
      if (refreshReportsResponse.ok) {
        const updatedReports = await refreshReportsResponse.json();
        setReportsDetails(updatedReports);
      } else {
        const errorMessages = await refreshReportsResponse.json();
        console.log("Error received:", errorMessages);
        throw new Error("Error refreshing reports");
      }
    } catch (error) {
      console.error(`An unexpected error occurred: ${error.message}`);
      setErrors(prevErrors => [...prevErrors, error.toString()]);
    }
  };

  const handleNewReportSuccess = (newReport) => {
    refreshReports(); // Refresh after a successful report submission to avoid async data issues
  };

  // Delete Report
  const handleDeleteReport = async (reportId) => {
    try{
      console.log("Report Id for Deletion:", reportId)
      const response = await fetch(`/reports/${reportId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${authInfo.accessToken}`,
        },
      });

      if (response.ok) {
        fetchData();
      } else {
        const errorMessages = await response.json();
        console.log("Delete failed:", errorMessages)
        throw new Error("Error deleting report");
      }

    } catch (error) {
      console.log("An error occurred:", error)
      setErrors(prevErrors => [...prevErrors, error.toString()]);
    }
  }

  // Update Report
  const [editingReport, setEditingReport] = useState(null);

  const handleUpdateReport = async (updatedValues, report_id) => {
    console.log("onUpdateReport called with:", updatedValues);
    try {
      const response = await fetch(`/reports/${report_id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${authInfo.accessToken}`,
        },
        body: JSON.stringify(updatedValues),
      });
  
      if (response.ok) {
        const updatedReport = await response.json();
        setReportsDetails((prevReports) => {
          return prevReports.map((report) => {
            if (report.id === report_id) {
              return updatedReport; // Replace current report in state with updated one
            } else {
              return report // otherwise, leave alone
            }
          });
        });
        setEditingReport(false);  // Hide the update form
      } else {
        const errorMessages = await response.json();
        console.error("Failed to update report", errorMessages);
        // setErrors(prevErrors => [...prevErrors, ...errorMessages.errors]);
        throw new Error("Error updating report");
      }
    } catch (error) {
      console.error("An error occurred:", error);
      setErrors(prevErrors => [...prevErrors, error.toString()]);
    }
  };
  
  return (
    <div>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <>
          <Header />
          <h1>Location Details</h1>
          <LocationCard location={locationDetails} />

          {authInfo.isLoggedIn ? (
            <>
              <h2>Add A New Report</h2>
              {!isFormVisible && <button onClick={toggleNewReportForm}>Add Your Report</button>}
              {isFormVisible && 
                <NewReportForm 
                  locationId={id} 
                  handleNewReportSuccess={handleNewReportSuccess} 
                  toggleNewReportForm={toggleNewReportForm}
                />
              }
            </>
          ) : (
            <button onClick={redirectToLoginPage}>Login to add a new report</button>
          )}

          <div>
          <h2>Reports for this location</h2>
          <ReportsByLocationId 
            reports={reportsDetails} 
            onDeleteReport={handleDeleteReport} 
            onUpdateReport={handleUpdateReport}
            editingReport={editingReport}
            setEditingReport={setEditingReport}
          />
          </div>

          <Footer />

          {/* {errors.map((err) => (
            <p key={err} style={{ color: "red" }}>
              {err}
            </p>
          ))} */}

          {/* {error && <div style={{ color: "red" }}>{errors}</div>} */}

          {errors.length > 0 && (
            <div style={{ color: "red" }}>
              {errors.map((err, index) => (
                <p key={index}>{err}</p>
              ))}
            </div>
          )}
          
        </>
      )}
    </div>
  );
}

export default LocationDetailsPage;
