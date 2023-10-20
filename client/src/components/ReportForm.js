import React, { useState, useEffect } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import styled from "styled-components";

function ReportForm({handleNewReport}){
    const [formData, setFormData] = useState()
    const [errors, setErrors] = useState([])

    useEffect(() => {
        // Fetch initial data from the database
        const fetchData = async () => {
          const response = await fetch("http://localhost:5555/locations");
          const data = await response.json();
          setFormData(data);
        };
    
        fetchData();
      }, []);

    const formSchema = Yup.object({
        user_id: Yup.number().required("Required"),
        location_id: Yup.number().required("Required"),
        // Add validation for reported features
        // Add validation for report photos
	});

    const formik = useFormik({
        initialValues: formData,
        validationSchema: formSchema,
        onSubmit: async (values) => {
                const config = await fetch("/reports", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(values),
                });
                const response = await fetch("/reports", config)

                if (response.ok) {
                    const newReport = await response.json();
                    handleNewReport(newReport)
                    setFormData({formData})
                    setErrors([]);
                } else{
                    const errorMessages = await response.json();
                    setErrors(errorMessages.errors)
                }
            }
    })
    return (
        <Form onSubmit={formik.handleSubmit}>
            <div>
            <label>Name ID</label>
            <input
            type="text"
            name="user_id"
            value={formik.values.user_id}
            onChange={formik.handleChange}
            />
            </div>
            <div>
            <label>Location ID</label>
            <input
            type="text"
            name="location_id"
            value={formik.values.location_id}
            onChange={formik.handleChange}
            />
            </div>
            {errors.map((err) => (
                <p key={err} style={{ color: "red" }}>
                {err}
                </p>
            ))}

        <button type="submit">Submit</button>

        </Form>
    );
}

export default ReportForm;

const Form = styled.form`
    display:flex;
    flex-direction:column;
    width: 400px;
    margin:auto;
    font-family:Arial;
    font-size:30px;
    input[type=submit]{
      background-color:#42ddf5;
      color: white;
      height:40px;
      font-family:Arial;
      font-size:30px;
      margin-top:10px;
      margin-bottom:10px;
    }
  `;
