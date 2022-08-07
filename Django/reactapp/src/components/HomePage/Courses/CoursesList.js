import React, { useState } from "react";
import CourseItem from "./CourseItem";

const CoursesList = (props) => {
  return (
    <div
      className="mt-3 scaled bg-white shadow-2xl rounded-lg px-8 pt-6 pb-8 mb-4 mr-20"
      style={{ width: "30rem" }}
    >
      <h3 className="block tracking-wide font-bold text-gray-700 mb-4">Your Classes</h3>
      {props.items.length !== 0 && <ul>
        {props.items.map((course) => (
          <CourseItem
            key={course.id}
            id={course.id}
            name={course.name}
            number={course.number}
            onRemoveCourse={props.onRemove}
          />
        ))}
      </ul>}
      {props.items.length === 0 && <p className="block tracking-wide text-2xl text-center mt-5">Enter your classes</p>}
    </div>
  );
};
export default CoursesList;
