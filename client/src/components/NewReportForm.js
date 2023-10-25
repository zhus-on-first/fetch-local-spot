import React, { useState, useEffect } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";


function NewReportForm({handleNewReport}){
    const [formData, setFormData] = useState({
        users: [],
        locations: [],
        features: [],
    })

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
          const featureResponse = await fetch("/locations");
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

    //   // Fetch location features by location_id
    //   const [selectedLocation, setSelectedLocation] = useState("")

    //   useEffect(() => {
    //     const fetchFeatures = async () => {
    //         console.log("Selected Location:", selectedLocation);
    //         if (selectedLocation) {
    //             const featureResponse = await fetch(`/location/<int:location_id>/features`)
    //             if (featureResponse.ok) {
    //                 const featureData = await featureResponse.json()
    //                 setFormData(prev => ({ ...prev, features: featureData}))
    //             } else {
    //                 const errorMessages = await featureResponse.json();
    //                 setErrors(errorMessages.errors);
    //             }
    //         }
    //     }
    //     fetchFeatures()
    //   }, [selectedLocation])
    

    const formSchema = Yup.object({
        user_id: Yup.number().required("Required"),
        location_id: Yup.number().required("Required"),
        reported_features: Yup.array().min(1, "Please select at least 1 feature"),
        photo_url: Yup.string().url("Must be a url")
	});
    
    const initialValues ={
        user_id: "",
        location_id: "",
        reported_features: [],
        photo_url: "",
        comment: ""
    }
    const formik = useFormik({
        initialValues,
        validationSchema: formSchema,
        onSubmit: async (values) => {
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
                    setFormData({formData})
                    setErrors([]);
                    formik.resetForm()
                } else{
                    const errorMessages = await response.json();
                    setErrors(errorMessages.errors)
                }
            }
    })

    return (
        <form onSubmit={formik.handleSubmit}>
            {/* show dropdown of available user name ids based on initial database fetch */}
            <div>
                <label>Name ID</label> 
                <select
                    name="user_id"
                    value={formik.values.user_id}
                    onChange={formik.handleChange}>
                    {formData.users && formData.users.map((users, index) => (
                        <option key={index} value={users.id}>{users.id}</option>
                    ))}
                </select>
            </div>

            {/* show dropdown of available location ids based on initial database fetch */}
            <div>
                <label>Location ID</label>
                <select
                    name="location_id"
                    value={formik.values.location_id}
                    onChange={formik.handleChange}>
                    {formData.locations && formData.locations.map((location, index) => (
                        <option key={index} value={location.id}>{location.id}</option>
                    ))}
                </select>
            </div>

            {/* show all possible features */}
            <div>
            <label>Reported Features</label>
            {formData.features && formData.features.map((feature, index) => (
                <div key={index}>
                    <input 
                        type="checkbox"
                        name="reported_features"
                        value={feature.id}
                        onChange={formik.handleChange}
                    />
                    <label>{feature.feature}</label>
                </div>
            ))}
            </div>

            {/* logic to upload photos */}

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

        </form>
    );
}

export default NewReportForm;