import React from "react";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";

function UpdateReportForm({report, setEditingReport, onUpdateReport}) { 

    const formSchema = Yup.object({
        user_id: Yup.number().required("Required"),
        location_id: Yup.number().required("Required"),
        // reported_features: Yup.array().min(1, "Please select at least 1 feature"),
        photo_url: Yup.string().url("Must be a url")
	});
    
    const initialValues ={
        user_id: report.user_id,
        location_id : report.location_id || "",
        reported_features: report.reported_features_names || [],
        comment: report.comment || "",
        photos: report.photos || []
    }

    // Handle deleting individual photos in update form
    const handleDeletePhoto = (index, setFieldValue) => {
        // Clone the existing photos array
        const newPhotos = [...report.photos];
        
        // Remove the photo at the given index
        newPhotos.splice(index, 1);
        
        // Update the Formik state
        setFieldValue("photos", newPhotos);
      };

    // Handle reported feature changes in update form
    const handleFeatureChange = (e, setFieldValue, values) => {
        const value = e.target.value;
        const checked = e.target.checked;

        // Copy current reported features array
        const updatedFeatures = [...values.reported_features];

        if (checked) {
            updatedFeatures.push(value);
        } else {
            const index = updatedFeatures.indexOf(value);
            if (index > -1) {
                updatedFeatures.splice(index, 1);
            }
        }

        // Update Formik state
        setFieldValue("reported_features", updatedFeatures);
    }

      
    return (
        <Formik
            initialValues={initialValues}
            validationSchema={formSchema}
            onSubmit={async (updatedValues, { setSubmitting }) => {
                console.log("Data to be sent to the backend:", updatedValues);
                await onUpdateReport(updatedValues, report.id)
                setEditingReport(null);
                setSubmitting(false);
            }}
        >

            {/* <Form>
                <Field type="number" name="user_id" />
                <Field type="number" name="location_id" />
                <Field type="check-box" name="reported_features" />
                <Field type="url" name="photo_url" />
                <Field type="text" name="comment" />
                <button type="submit">Save</button>
                <button type="button" onClick={() => setEditingReport(null)}>Cancel</button>
            </Form> */}

            {({ setFieldValue, values, errors }) => {
                console.log("Formik errors:", errors);
                return (
                    <Form>
                        {/* User ID Field */}
                        <div>
                            <label htmlFor="user_id">User ID--do NOT change</label>
                            <Field id="user_id" name="user_id" type="text" />
                        </div>

                        {/* Location ID Field */}
                        <div>
                            <label htmlFor="location_id">Location ID--do NOT change</label>
                            <Field id="location_id" name="location_id" type="text" />
                        </div>

                        {/* Comment Field */}
                        <div>
                            <label htmlFor="comment">Comment</label>
                            <Field id="comment" name="comment" type="text" />
                        </div>

                        {/* Reported Features Field */}
                        <div>
                            <label htmlFor="reported_features">Reported Features</label>
                            {values.reported_features && values.reported_features.length > 0 ? (
                                report.reported_features_names.map((feature, index) => (
                                    <div key={index}>
                                        <label>
                                            <Field 
                                                type="checkbox" 
                                                name="reported_features" 
                                                value={feature} 
                                                onChange={e => handleFeatureChange(e, setFieldValue, values)}
                                            />
                                            {feature}
                                        </label>
                                    </div>
                                ))
                            ) : (
                                <p>No reported features available to edit.</p>
                            )}
                        </div>

                        {/* Photos*/}
                        <div>
                            <label htmlFor="photos">Photos:</label>
                            {values.photos ? (
                                values.photos.map((photo, index) => (
                                    <div key={index}>
                                    <img key={index} src={photo.photo_url} alt={`Uploaded ${index}`} />
                                    <button type="button" onClick={() => handleDeletePhoto(index, setFieldValue)}>Delete</button>
                                    </div>
                                ))
                            ) : (
                                <p>No photos have been uploaded for you to edit.</p>
                            )}
                            
                            <Field id="newPhotos" name="newPhotos" type="file" multiple />
                        </div>

                        <button type="submit">Submit Update</button>
                        <button type="button" onClick={() => setEditingReport(null)}>Cancel</button>
                    </Form>

                )

                }
            }
            
        </Formik>
    );
}

export default UpdateReportForm;

// Patch object to use with test
// {
//     "user_id": 1,
//     "location_id": 8,
//     "comment": "tester 10/31 17:52",
//     "reported_features": [],
//     "photos": []
// }