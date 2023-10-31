import React from "react";
import UpdateReportForm from "./UpdateReportForm";

function ReportsByLocationId({ reports, onDeleteReport, onUpdateReport, editingReport, setEditingReport }) {
    // console.log("Reports by location array:", reports);
    // console.log("Currently editing report with ID:", editingReport);

    return (
        <div>
          {reports.map((report) => {
            console.log("Report ID from the report object:", report.id);
            console.log("Currently editing report with ID:", editingReport);

            return (
                <div key={report.id}>

                  {/* Static Report Details */}
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
              
              // Code below hides report that's being edited:
              // <div key={report.id}>
              //   {editingReport === report.id ? (
              //     <UpdateReportForm
              //       report={report}
              //       onUpdateReport={() => onUpdateReport(report.id)}
              //       setEditingReport={setEditingReport}
              //       locationId={report.location_id}
              //     />
              //   ) : (
              //     <>
              //       <h4>Report ID: {report.id}</h4>
              //       <p>User ID: {report.user_id}</p>
              //       <p>Location ID (HERE JUST TO CONFIRM LOCATION): {report.location_id}</p>
              //       <p>User Name: {report.username}</p>
              //       <p>User's Reported Features: {report.reported_features_names}</p>
              //       <p>Comment: {report.comment}</p>
              //       <p>Photos: {
              //         report.photos ?
              //           report.photos.map((photo) => (
              //             <img key={photo.id} src={photo.photo_url} alt="Reported photos"></img>
              //         ))
              //         : "No photos available"
              //         }</p>
              //       <button onClick={() => onDeleteReport(report.id)}>Delete This Report</button>

              //     </>
              //   )}
              //                       {editingReport === report.id ? (
              //         <button onClick={() => {
              //           console.log('Cancel button clicked'); 
              //           setEditingReport(null)}}>Cancel</button>
              //       ) : (
              //         <button onClick={() => setEditingReport(report.id)}>Update this Report</button>
              //       )}
              // </div>
            );
          })}
        </div>
    );
}

export default ReportsByLocationId;
