import React from "react";

function ReportsByLocationId({ reports, onDeleteReport }) {
    console.log("Reports by location array:", reports);
    
    return (
        <div>
          {reports.map((report) => (
            <div key={report.id}>
              <h4>Report ID: {report.id}</h4>
              <p>User ID: {report.user_id}</p>
              <p>Location ID (HERE JUST TO CONFIRM LOCATION): {report.location_id}</p>
              <p>User Name: {report.username}</p>
              <p>User's Reported Features: {report.reported_features_names}</p>
              <p>Comment: {report.comment}</p>
              <p>Photos: {
                report.photos ?
                  report.photos.map((photo) => (
                    <img key={photo.id} src={photo.photo_url} alt="Reported photos"></img>
                ))
                : "No photos available"
                }</p>
                <button onClick={() => onDeleteReport(report.id)}>Delete This Report</button>
            </div>
          ))}
        </div>
    );
}

export default ReportsByLocationId
