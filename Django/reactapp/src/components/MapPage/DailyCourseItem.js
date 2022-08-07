import React from "react";
import './DailyCourseContainer.css';

const DailyCourseItem = (props) => {
  const infoClickHandler = () => {
    console.log("more info needed");
  };
  return (
    <div className="bg-blue-500 shadow-md rounded-lg px-3 pt-1 pb-1 mb-3 hover:bg-blue-700 transition ease-in-out delay-150 duration-300">
      <h5 className="text-white block tracking-wide font-semi-bold course-list mt-1">
        {props.name}
        <svg
          class="h-5 w-5 text-white float-right hover:scale-110 transition ease-in-out duration-100"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          onClick={infoClickHandler}
        >
          {" "}
          <circle cx="12" cy="12" r="10" />{" "}
          <line x1="12" y1="16" x2="12" y2="12" />{" "}
          <line x1="12" y1="8" x2="12.01" y2="8" />
        </svg>
      </h5>
    </div>
  );
};

export default DailyCourseItem;
