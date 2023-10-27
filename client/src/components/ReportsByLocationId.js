import React from "react";

function ReportsByLocationId({ reports }) {
    console.log("Reports array:", reports);
    
    return (
        <div>
          {reports.map((report, index) => (
            <div key={index}>
              <h4>Report ID: {report.id}</h4>
              <p>User ID: {report.user_id}</p>
              <p>Location ID: {report.location_id}</p>
              <p>Comment: {report.comment}</p>
            </div>
          ))}
        </div>
    );
}

export default ReportsByLocationId
