import React, { useEffect, useState } from "react";
import NewReportForm from "../components/NewReportForm";
import LocationList from "../components/LocationList"
import LocationForm from "../components/LocationForm";

function LocationDetailsPage({id}) {
    const [locationDetails, setLocationDetails] = useState({});
    const [reports, setReports] = useState([])
    const [errors, setErrors] = useState([])
    const [confirmationMessage, setConfirmationMessage] = useState("");
    
    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch(`http://localhost:5555/locations/${id}`);
            if (response.ok) {
              const data = await response.json();
              setLocationDetails(data.location);
              setReports(data.reports);
            } else{
                const errorMessages = await response.json();
                setErrors(errorMessages.errors)
            }
        };
        fetchData();
    }, [id]);

    useEffect(() => {
        const fetchReports = async () => {
          const response = await fetch("http://localhost:5555/reports");
          if (response.ok) {
            const data = await response.json();
            setReports(data);
          } else {
                const errorMessages = await response.json();
                setErrors(errorMessages.errors)
            }
        }
        fetchReports();
      }, []);
    

    const handleNewReport = (newReport) => {
        setReports([...reports, newReport]);
        setConfirmationMessage("Report submitted successfully!");
      };

    return (
        <div>
            <h1>Location Details</h1>
            <div>
            <p>insert location details here</p>
            </div>
    
            <div>{confirmationMessage}</div>
            
            <h2>Existing Reports</h2>
            <ul>
            {reports.map((report, index) => (
                <li key={index}>
                <p>insert report details here</p>
                </li>
            ))}
            </ul>
    
            <h2>Submit a New Report</h2>
        <NewReportForm handleNewReport={handleNewReport} />

        {errors.map((err) => (
                <p key={err} style={{ color: "red" }}>
                {err}
                </p>
            ))}
      </div>
    );
};


export default LocationDetailsPage;