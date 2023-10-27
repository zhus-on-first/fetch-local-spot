import React, { useEffect, useState } from "react";
import ReportCard from "./ReportCard";

function ReportList() {
    const [reports, setReports] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("/reports");
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                const apiData = await response.json();
                console.log(apiData)
                setReports(apiData);
            } catch (error) {
                console.error("There was a problem with the fetch:", error)
            }
        };
        fetchData();
    }, []); // empty array makes sure effect runs only once when it mounts.

    return (
        <div>
            {/* {reports.map((report) => (
                <reportCard key={report.id} report={report} />
            ))} */}

            {reports.map((report) => {
                console.log("Current report:", report);
                return (
                <ReportCard 
                key={report.id} 
                report={report} 
                />)
            }
            )})
        </div>
    );
}

export default ReportList;