import React, { useState } from "react";
import { Form } from "react-bootstrap";
import axios from "axios";

const YearSem = (props) => {
  const [enteredYear, setEnteredYear] = useState("");
  const [enteredSem, setEnteredSem] = useState("");

  const selectedYearHandler = (event) => {
    setEnteredYear(event.target.value);
  };
  const selectedSemHandler = (event) => {
    setEnteredSem(event.target.value);
  };
  const YSSubmitHandler = async (event) => {
    event.preventDefault();

    const yearSem = {
      year: enteredYear,
      semester: enteredSem,
    };

    setDisab(true);
    props.onSubmitDisab(true);
    
    console.log("Sending a POST API Call");

    axios ({
      method: "POST",
      url: "http://127.0.0.1:8000/api/yearsem/",
      data: yearSem,
    }).then((response) => {
      console.log(response);
    });

  };
  const [disab, setDisab] = useState(false);
  return (
    <div class="w-full max-w-md">
      <Form
        className="bg-white shadow-2xl rounded-lg px-8 pt-6 pb-8 mb-4"
        onSubmit={YSSubmitHandler}
      >
        <Form.Group>
          <Form.Label className="block uppercase tracking-wide text-gray-700 text-md font-bold mb-0">
            Semester
          </Form.Label>
          <Form.Select
            name="sem"
            className="block tracking-wide h-11"
            onChange={selectedSemHandler}
            required
            disabled={disab}
          >
            <option value="" disabled selected hidden>
              Select
            </option>
            <option value="Fall">Fall</option>
            <option value="Spring">Spring</option>
            <option value="Summer">Summer</option>
            <option value="Winter">Winter</option>
          </Form.Select>
          <Form.Label className="block uppercase tracking-wide text-gray-700 text-md font-bold mb-0 mt-3">
            Year
          </Form.Label>
          <Form.Control
            className="block tracking-wide h-11"
            name="year"
            type="number"
            placeholder="ex. 2022"
            min="2004"
            max="2022"
            onChange={selectedYearHandler}
            required
            disabled={disab}
          ></Form.Control>
          <button
            type="submit"
            className={`bg-blue-500 form-button mt-3 transition ease-in-out delay-150 hover:scale-105 duration-300 ${
              disab ? "opacity-50 cursor-not-allowed" : ""
            }`}
            disabled={disab}
          >
            Continue
          </button>
        </Form.Group>
      </Form>
    </div>
  );
};

export default YearSem;
