import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./CourseItem.css";
import CloseButton from "react-bootstrap/CloseButton";

const CourseItem = (props) => {
  return (
    <div className="bg-blue-500 shadow-md rounded-lg px-4 pt-2 pb-2 mb-3 hover:bg-blue-700 transition ease-in-out delay-150 hover:scale-105 duration-300">
      <h5 className="text-white block tracking-wide uppercase font-semi-bold">
        {props.name} {props.number}
        <CloseButton
          className="float-right"
          onClick={() => props.onRemoveCourse(props.id)}
        />
      </h5>
    </div>
  );
};

export default CourseItem;
