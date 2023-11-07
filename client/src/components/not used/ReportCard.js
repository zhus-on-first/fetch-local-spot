import React from "react";

function ReportCard({ report }) {
    console.log("Report object:", report);
    
    return (
        <div>
            <h4>Report ID: {report.id}</h4>
            <p>User ID: {report.user_id}</p>
            <p>Location ID: {report.location_id}</p>
            <p>Comment: {report.comment}</p>
        </div>
    );
}


export default ReportCard;