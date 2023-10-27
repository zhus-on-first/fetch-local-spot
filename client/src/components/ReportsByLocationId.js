import React from "react";

function ReportsByLocationId({ reports }) {
    console.log("Reports array:", reports);
    
    return (
        <div>
          {reports.map((report, id) => (
            <div key={id}>
              <h4>Report ID: {report.id}</h4>
              <p>User ID: {report.user_id}</p>
              <p>Location ID: {report.location_id}</p>
              <p>User Name: {report.username}</p>
              <p>User's Reported Features: {report.reported_features_names}</p>
              <p>Comment: {report.comment}</p>
              <p>Photos: {report.photos.map((photo) => (
                <img key={photo.id} src={photo.photo_url} alt="Reported photos"></img>
                ))}
              </p>
            </div>
          ))}
        </div>
    );
}

export default ReportsByLocationId
