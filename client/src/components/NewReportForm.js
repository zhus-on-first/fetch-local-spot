import React, { useState, useEffect } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";


function NewReportForm({handleNewReport, toggleForm, locationId}){
    const [formData, setFormData] = useState({
        users: [],
        locations: [],
        features: [],
    })

    const [isSubmitted, setIsSubmitted] = useState(false);

    const [errors, setErrors] = useState([])

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
        reported_features: Yup.array().min(1, "Please select at least 1 feature"),
        photo_url: Yup.string().url("Must be a url")
	});
    
    const initialValues ={
        user_id: "",
        location_id : locationId || "",
        reported_features: [],
        photo_url: "",
        comment: ""
    }
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
                    handleNewReport(newReport)
                    setErrors([]);
                    formik.resetForm();
                    setIsSubmitted(true);
                } else {
                    const errorMessages = await response.json();
                    setErrors(errorMessages.errors)
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
                    <div>{formik.errors.user_id}</div>
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
            {/* {formData.features && formData.features.map((feature, index) => (

                <div key={feature.id}>
                    <input 
                        type="checkbox"
                        name="reported_features"
                        value={feature.id}
                        onChange={formik.handleChange}
                    />
                    <label>{feature.feature}</label>
                </div>
            ))} */}

            {formData.features && formData.features.map((feature) => {
            // Log current feature object to see structure
                console.log("Current feature:", feature);

                return (
                    <div key={feature.id}>
                        <input 
                            type="checkbox"
                            name="reported_features"
                            value={feature.id}
                            onChange={formik.handleChange}
                        />
                        <label>{feature.id}: {feature.name}</label>
                    </div>
                );
            })}
            </div>

            {/* Display Upload photos */}
            <div>
                <label>Upload Photos:</label>
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
            

            {errors.map((err) => (
                <p key={err} style={{ color: "red" }}>
                {err}
                </p>
            ))}

        <button type="submit">Submit</button>
        <button type="button" onClick={toggleForm}>Cancel</button>

        {isSubmitted && <p>Your report has been successfully submitted!</p>}

        </form>
    );
}

export default NewReportForm;


// What a POST object looks like
// {
//     "user_id": 1,
//     "location_id": 2,
//     "reported_features": [1, 3, 4],
//     "photo_url": "http://www.photo.com/1.jpg",
//     "comment": "Great place!"
//   }