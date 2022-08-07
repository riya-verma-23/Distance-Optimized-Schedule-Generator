import React from "react";
import "./ScheduleList.css";
import ScheduleItem from "./ScheduleItem";
const ScheduleList = (props) => {
  return (
    <div className="table-size">
      <table class="table-bordered bg-white shadow-2xl">
        <thead class="bg-blue-600">
          {props.courses.map((schedule) => (
            <th scope="col">{schedule}</th>
          ))}
        </thead>
        <tbody>
          {Object.entries(props.schedules).map(
            ([key, schedule]) => (
              <ScheduleItem schedule={schedule} id={key} onView={props.onView} />
            ))}
        </tbody>
      </table>
    </div>
  );
};
export default ScheduleList;
