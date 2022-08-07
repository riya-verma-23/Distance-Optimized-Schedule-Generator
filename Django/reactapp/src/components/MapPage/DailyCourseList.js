import DailyCourseItem from "./DailyCourseItem";
import React from "react";
import './DailyCourseContainer.css';

const DailyCourseList = (props) => {
  return (
    <div className="bg-slate-400 shadow-2xl rounded-lg px-6 pt-6 pb-6">
      <h3 className="text-white block tracking-wide uppercase course-list font-semi-bold rounded-lg px-8 pt-2 pb-2 mb-4 text-center bg-slate-500">
          {props.day}
      </h3>
      {props.courses.map((course) => (<DailyCourseItem name={course}/>))}
      
    </div>
  );
};

export default DailyCourseList;
