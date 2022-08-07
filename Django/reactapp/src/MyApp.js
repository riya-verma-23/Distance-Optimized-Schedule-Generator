import "./App.css";
import { Route, Routes, useNavigate } from "react-router-dom";
import Home from "./components/HomePage/Home";
import ScheduleList from "./components/BestSchedulePage/ScheduleList";
import axios from "axios";
import React, { useState } from "react";
import DailyCourseContainer from "./components/MapPage/DailyCourseContainer";

const MyApp = () => {
  const navigate = useNavigate();

  const [schedules, setSchedules] = useState({});
  const [courses, setCourses] = useState([]);

  let courses_header = [];

  const FormSubmitHandler = (course_list) => {
    course_list.forEach((course) => {
      courses_header.push(course.name + " " + course.number);
    });

    let course_post_data = courses_header;
    courses_header = courses_header.concat(" ");
    setCourses(courses_header);

    axios({
      method: "POST",
      url: "http://127.0.0.1:8000/api/sendcourse/",
      data: course_post_data,
    }).then((response) => {
      console.log(response);
    });

    axios.get("http://127.0.0.1:8000/api/getcourselist/").then((response) => {
      console.log(response);
      setSchedules(response.data);
      navigate("/best-schedules");
    });
  };
  const [dailySchedule, setDailySchedule] = useState([]);
  const [mapLinks, setMapLinks] = useState([]);

  const displayDailyScheduleHandler = (dailySchedule, locations) => {
    setDailySchedule(dailySchedule);
    setMapLinks(locations);
    navigate("./best-schedules/view-schedule");
  };

  return (
    <div class="App-header">
      <div className="bg-blue-900 pb-2 pt-1">
        <section class="hero container max-w-screen-lg mx-auto pb-2 flex justify-center mt-2">
          <img
            className="left-60"
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Illinois_Fighting_Illini_logo.svg/1200px-Illinois_Fighting_Illini_logo.svg.png"
            width="27px"
            height="27px"
          />
        </section>
        <h1 className="text-center text-4xl font-sans text-white font-semi-bold">
          UIUC Schedule Generator
        </h1>
      </div>

      <Routes>
        <Route path="/" element={<Home form_submit={FormSubmitHandler} />} />
        <Route
          path="/best-schedules"
          element={
            <ScheduleList
              courses={courses}
              schedules={schedules}
              onView={displayDailyScheduleHandler}
            />
          }
        />
        <Route
          path="/best-schedules/view-schedule"
          element={
            <DailyCourseContainer courses={dailySchedule} links={mapLinks} />
          }
        />
      </Routes>
    </div>
  );
};

export default MyApp;
