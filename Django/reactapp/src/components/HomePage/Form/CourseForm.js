import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Form } from "react-bootstrap";

const CourseForm = (props) => {
  const [name, setName] = useState("");
  const [number, setNumber] = useState("");

  const nameChangeHandler = async (event) => {
    setName(event.target.value);
    console.log(event.target.value);
  };
  const numberChangeHandler = (event) => {
    setNumber(event.target.value);
    console.log(event.target.value);
  };
  const submitHandler = (event) => {
    event.preventDefault();
    const courseData = {
      name: name,
      number: number,
    };
    props.onSaveCourseData(courseData);
    setName("");
    setNumber("");
  };
  return (
    <div className="w-full max-w-md">
      <Form className="bg-white shadow-2xl rounded-lg px-8 pt-6 pb-8 mb-3" onSubmit={submitHandler}>
        <Form.Group>
          <Form.Label className="block uppercase tracking-wide text-gray-700 text-md font-bold mb-0">Name</Form.Label>
          <Form.Control
            className="block tracking-wide h-11"
            type="text"
            maxLength={4}
            pattern="[a-zA-Z]+" 
            title="Only alphabets are allowed"
            minLength={2}
            placeholder="ex. MATH"
            disabled={props.dis}
            onChange={nameChangeHandler}
            required
            value={name}
          ></Form.Control>
          <Form.Label className="block uppercase tracking-wide text-gray-700 text-md font-bold mb-0 mt-3">Number</Form.Label>
          <Form.Control
            className="block tracking-wide h-11"
            type="number"
            min="100"
            max="999"
            placeholder="ex. 241"
            disabled={props.dis}
            onChange={numberChangeHandler}
            required
            value={number}
          ></Form.Control>
          <button type="submit" className={`bg-blue-500 form-button mt-3 ${
            props.dis ? "opacity-50 cursor-not-allowed" : "transition ease-in-out delay-150 hover:scale-105 duration-300"
          }`} disabled={props.dis}>Add Course</button>
        </Form.Group>
      </Form>
    </div>
  );
};
export default CourseForm;
