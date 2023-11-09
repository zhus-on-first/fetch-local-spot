import React, { useState, useEffect } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";


function NewReportForm({handleNewReportSuccess, toggleNewReportForm, locationId}){
    const [formData, setFormData] = useState({
        users: [],
        locations: [],
        features: [],
    })

    const [isSubmitted, setIsSubmitted] = useState(false);

    const [errors, setErrors] = useState("")

    useEffect(() => {
        const fetchData = async () => {
            
          // Fetch locations
          const locationResponse = await fetch("/locations");
          if (locationResponse.ok){
            const locationData = await locationResponse.json();
            setFormData(prev => ({ ...prev, locations: locationData}))
          } else {
            const errorMessages = await locationResponse.json();
            setErrors(errorMessages.errors);
          }

          // Fetch user IDs
          const userResponse = await fetch("/users");
          if (userResponse.ok){
            const userData = await userResponse.json();
            setFormData(prev => ({ ...prev, users: userData}))
          } else {
            const errorMessages = await userResponse.json();
            setErrors(errorMessages.errors);
          }

          // Fetch features
          const featureResponse = await fetch("/features");
          if (featureResponse.ok){
            const featureData = await featureResponse.json();
            setFormData(prev => ({ ...prev, features: featureData}))
          } else {
            const errorMessages = await featureResponse.json();
            setErrors(errorMessages.errors);
          }

        }
        fetchData();
      }, []);

    const formSchema = Yup.object({
        user_id: Yup.number().required("Required"),
        location_id: Yup.number().required("Required"),
        reported_features_ids: Yup.array().of(Yup.number()).min(1, "Please select at least one feature"),
        photo_urls: Yup.array().of(Yup.string().url("Must be a valid URL")),
        comment: Yup.string().nullable()
    });
    
    const initialValues = {
        user_id: "",
        location_id: locationId || "",
        reported_features_ids: [], 
        photo_urls: [],
        comment: ""
    }
    console.log('Formik initial values:', initialValues);

    const formik = useFormik({
        initialValues,
        validationSchema: formSchema,
        onSubmit: async (values) => {
            console.log("Form values being posted:", values)
            try {
                const response = await fetch("/reports", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(values),
                });

                if (response.ok) {
                    const newReport = await response.json();
                    console.log('New Report:', newReport);
                    handleNewReportSuccess(newReport)
                    setErrors("");
                    formik.resetForm();
                    setIsSubmitted(true);
                } else {
                    if(response.status === 401) {
                        setErrors('You are not authorized to submit this report. Please log in.');
                    } else {
                        const errorMessages = await response.json();
                        setErrors(errorMessages.message || 'An unexpected error occurred.');
                    }
                }
            } catch (error) {
                console.log("An error occurred:", error);
                setErrors(["An unexpected error occurred"])
            } 
        },
    });

    useEffect(() => {
        if (isSubmitted) {
            setTimeout(() => {
                setIsSubmitted(false);
            }, 5000)
        }
    }, [isSubmitted]);

    const handleFeatureChange = (e) => {
        const { value, checked } = e.target;
        const { reported_features_ids } = formik.values;
    
        if (checked) {
            formik.setFieldValue('reported_features_ids', [...reported_features_ids, parseInt(value)]);
        } else {
            formik.setFieldValue('reported_features_ids', reported_features_ids.filter((id) => id !== parseInt(value)));
        }
    }
    
    const handlePhotoUrlChange = (e, index) => {
        const newPhotoUrls = [...formik.values.photo_urls];
        newPhotoUrls[index] = e.target.value;
        formik.setFieldValue("photo_urls", newPhotoUrls);
    };

    return (
        <form onSubmit={formik.handleSubmit}>
            {/* Show dropdown of available user name ids based on initial database fetch */}
            <div>
                <label>Name ID</label> 
                <select
                    name="user_id"
                    value={formik.values.user_id}
                    onChange={formik.handleChange}>
                    <option value="" label="Select User ID" />
                    {formData.users && formData.users.map((users, index) => (
                        <option key={index} value={users.id}>{users.id}</option>
                    ))}
                </select>
                {formik.touched.user_id && formik.errors.user_id ? (
                    <div>{formik.errors.user_id}: Please select a user id.</div>
                ): null}
            </div>

            {/* Show dropdown of available location ids based on initial database fetch */}
            <div>
                <label>Location ID (DO NOT change)</label>
                <select
                    name="location_id"
                    value={formik.values.location_id}
                    onChange={formik.handleChange}>
                    {formData.locations && formData.locations.map((location, index) => (
                        <option key={index} value={location.id}>{location.id}</option>
                    ))}
                </select>
            </div>

            {/* Show all possible features */}
            <div>
                <label>Reported Features</label>

                {formData.features && formData.features.map((feature) => {
                    return (
                        <div key={feature.id}>
                            <input 
                                type="checkbox"
                                name="reported_features_ids"
                                value={feature.id}
                                checked={formik.values.reported_features_ids.includes(feature.id)}
                                onChange={handleFeatureChange}
                            />
                            <label>{feature.id}: {feature.name}</label>
                        </div>
                    );
                })}
            </div>

            {/* Display Upload photos */}
            <div>
                <label>Photo URLs:</label>
                {formik.values.photo_urls.map((url, index) => (
                    <input 
                        key={index}
                        type="text"
                        name={`photo_urls[${index}]`}
                        value={url}
                        onChange={e => handlePhotoUrlChange(e, index)}
                    />
                ))}
                <button type="button" onClick={() => formik.setFieldValue('photo_urls', [...formik.values.photo_urls, ''])}>Add Photo URL</button>
            </div>

            {/* Display Comment */}
            <div>
                <label>Comment</label>
                <input
                type="text"
                name="comment"
                value={formik.values.comment}
                onChange={formik.handleChange}
                />
            </div>
            
{/* 
            {errors.map((err) => (
                <p key={err} style={{ color: "red" }}>
                {err}
                </p>
            ))} */}

        {/* Display a single error message */}
        {errors && <div style={{ color: "red" }}>{errors}</div>}


        <button type="submit">Submit</button>
        <button type="button" onClick={toggleNewReportForm}>Cancel</button>

        {isSubmitted && <p>Your report has been successfully submitted!</p>}

        </form>
    );
}

export default NewReportForm;


// What a POST object looks like
// {
//     "user_id": 1,
//     "location_id": 2,
//     "reported_features_ids": [1, 3, 4],
//     "photo_url": "http://www.photo.com/1.jpg",
//     "comment": "Great place!"
//   }