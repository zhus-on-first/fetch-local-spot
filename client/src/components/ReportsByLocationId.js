import React from "react";
import UpdateReportForm from "./UpdateReportForm";

function ReportsByLocationId({ reports, onDeleteReport, onUpdateReport, editingReport, setEditingReport }) {
    // console.log("Reports by location array:", reports);
    // console.log("Currently editing report with ID:", editingReport);

    return (
        <div>
          {reports.map((report) => {
            console.log('Report in list:', report);
            console.log("Report ID from the report object:", report.id);
            console.log("Currently editing report with ID:", editingReport);

            return (
                <div key={report.id}>

                  {/* Static Report Details */}
                  <h4>Report ID: {report.id}</h4>
                  <p>User ID: {report.user?.id}</p>
                  <p>Location ID (HERE JUST TO CONFIRM LOCATION): {report.location_id}</p>
                  <p>User Name: {report.user?.username}</p>
                  <p>User's Reported Features:</p>
                    {report.reported_features_names && report.reported_features_names.length > 0 ? (
                      <ul>
                        {report.reported_features_names.map((rfn, index) => (
                          <li key={index}>{rfn}</li>
                        ))}
                      </ul>
                    ) : <p>No reported features</p>}
                  <p>Comment: {report.comment}</p>
                  <p>Photos: </p>
                    {report.reported_photos && report.reported_photos.length > 0 ? (
                      <ul>
                          {report.reported_photos.map((photo) => (
                            <img key={photo.id} src={photo.photo_url} alt="Reported photos" />
                      ))}
                      </ul>
                    ) : <p>No photos available</p>}
                  <button onClick={() => onDeleteReport(report.id)}>Delete This Report</button>
                  <button onClick={() => setEditingReport(report.id)}>Update this Report</button>
                  
                  {/* Conditionally Render Update Report Form */}
                  {editingReport === report.id && (
                    <UpdateReportForm
                      report={report}
                      onUpdateReport={onUpdateReport}
                      setEditingReport={setEditingReport}
                      locationId={report.location_id}
                    />
                  )}
              </div>
              
            );
          })}
        </div>
    );
}

export default ReportsByLocationId;
