import React, { useState } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
// import styled from "styled-components";

function LocationForm({handleNewLocation}) {
  const [formData, setFormData] = useState({
    name: "",
    address: "",
    phone: "",
    location_type_id: null,
  });
  
  const [errors, setErrors] = useState([]);

  const formSchema = Yup.object({
    name: Yup.string().required("Required"),
    address: Yup.string().required("Required"),
    phone: Yup.string().required("Required"),
    location_type_id: Yup.number().nullable(),
  });

  const formik = useFormik({
    initialValues: formData,
    validationSchema: formSchema,
    onSubmit: async (values) => {
      const config = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(values),
      };

      const response = await fetch("http://localhost:5555/locations", config);

      if (response.ok) {
        const newLocation = await response.json();
        handleNewLocation(newLocation)
        setFormData({
          name: "",
          address: "",
          phone: "",
          location_type_id: null,
        });
        setErrors([]);
      } else {
        const errorMessages = await response.json();
        setErrors(errorMessages.errors);
      }
    },
  });

  return (
    <form onSubmit={formik.handleSubmit}>
      <div>
        <label>Location Type</label>
        <select
          name="location_type_id"
          value={formik.values.location_type_id}
          onChange={formik.handleChange}
        >
          <option value="" label="Select type" />
          <option value="1" label="Hike" />
          <option value="2" label="Food Spot" />
          <option value="3" label="Ride" />
        </select>
      </div>
      <div>
        <label>Name</label>
        <input
          type="text"
          name="name"
          value={formik.values.name}
          onChange={formik.handleChange}
        />
      </div>
      <div>
        <label>Address</label>
        <input
          type="text"
          name="address"
          value={formik.values.address}
          onChange={formik.handleChange}
        />
      </div>
      <div>
        <label>Phone</label>
        <input
          type="text"
          name="phone"
          value={formik.values.phone}
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

export default LocationForm;

// const Form = styled.form`
//   display: flex;
//   flex-direction: column;
//   width: 400px;
//   margin: auto;
//   font-family: Arial;
//   font-size: 30px;
//   input[type="submit"] {
//     background-color: #42ddf5;
//     color: white;
//     height: 40px;
//     font-family: Arial;
//     font-size: 30px;
//     margin-top: 10px;
//     margin-bottom: 10px;
//   }
// `;