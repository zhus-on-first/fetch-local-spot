import React from "react";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";

function UpdateReportForm({report, setEditingReport, onUpdateReport}) { 

    const formSchema = Yup.object({
        user_id: Yup.number().required("Required"),
        location_id: Yup.number().required("Required"),
        reported_features: Yup.array().min(1, "Please select at least 1 feature"),
        photo_url: Yup.string().url("Must be a url")
	});
    
    const initialValues ={
        user_id: report.user_id,
        location_id : report.location_id || "",
        reported_features: report.reported_features_names,
        comment: report.comment || "",
        photos: report.photos || []
    }

    const handleDeletePhoto = (index, setFieldValue) => {
        // Clone the existing photos array
        const newPhotos = [...report.photos];
        
        // Remove the photo at the given index
        newPhotos.splice(index, 1);
        
        // Update the Formik state
        setFieldValue('photos', newPhotos);
      };
      
    return (
        <Formik
            initialValues={initialValues}
            validationSchema={formSchema}
            onSubmit={async (updatedValues, { setSubmitting }) => {
                await onUpdateReport(updatedValues)
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

                {/* Photos*/}
                <div>
                    <label htmlFor="photos">Photos:</label>
                    {report.photos ? (
                        report.photos.map((photo, index) => (
                            <div key={index}>
                            <img key={index} src={photo.photo_url} alt={`Uploaded ${index}`} />
                            <button type="button" onClick={() => handleDeletePhoto(index)}>Delete</button>
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