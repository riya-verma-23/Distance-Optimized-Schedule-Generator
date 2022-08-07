import React, { useState } from "react";
import DailyCourseList from "./DailyCourseList";
import { Container, Row, Col } from "react-bootstrap";
import MapImage from "./MapImage";
import { useNavigate } from "react-router-dom";
import "./DailyCourseContainer.css";

const DailyCourseContainer = (props) => {
  const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];

  const [day, setDay] = useState(0);

  const prevDayHandler = () => {
    if (day === 0) {
      setDay(4);
    } else {
      setDay((prevDay) => (prevDay - 1) % 5);
    }
  };
  const nextDayHandler = () => {
    setDay((prevDay) => (prevDay + 1) % 5);
  };

  let prevButton = (
    <button
      className="bg-blue-500 form-button float-left mt-48 ml-5 hover:scale-105"
      onClick={prevDayHandler}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-4 w-4"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fillRule="evenodd"
          d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
          clipRule="evenodd"
        />
      </svg>
    </button>
  );
  let nextButton = (
    <button
      className="bg-blue-500 form-button float-right mt-48 mr-5 hover:scale-105"
      onClick={nextDayHandler}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-4 w-4"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fillRule="evenodd"
          d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
          clipRule="evenodd"
        />
      </svg>
    </button>
  );
  const navigate = useNavigate();
  const onClickHandler = () => {
    navigate(-1);
  };
  let viewAnotherButton = (
    <button
      onClick={onClickHandler}
      className="bg-slate-700 form-button hover:scale-105 transition -translate-y-10 ease-in-out button-center float-right duration-200"
    >
      View Another Schedule
    </button>
  );
  return (
    <div className="map-container mt-4">
      <span>{prevButton}</span>
      <span>{nextButton}</span>
      <Container>
        <Row>
          <Col md="auto">
            <div className="bg-slate-700 rounded-lg shadow-2xl px-3 mb-3 text-position">
              <h1 className="text-white text-center px-1 pb-1 pt-1 text-2xl">
                Your Daily Schedule
              </h1>
            </div>
          </Col>
        </Row>
        <Row>
          <Col xs={8}>
            <MapImage mapLink={props.links[day]} />
          </Col>
          <Col>
            <DailyCourseList day={days[day]} courses={props.courses[day]} />
          </Col>
        </Row>
        {viewAnotherButton}
      </Container>
    </div>
  );
};

export default DailyCourseContainer;
