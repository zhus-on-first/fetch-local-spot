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
                    <Field id="newPhotos" name="newPhotos" type="file" multiple />
                </div>

                <button type="submit">Click Here to Finalize Update</button>
                <button type="button" onClick={() => setEditingReport(null)}>Cancel</button>
            </Form>
            
            
        </Formik>
    );
}

export default UpdateReportForm;