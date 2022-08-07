import MyForm from "./Form/Form";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import CoursesList from "./Courses/CoursesList";
import React, { useState } from "react";

const  Home = (props) => {
  const [courses, setCourses] = useState([]);

  const addCourseHandler = (course) => {
    setCourses((prevCourses) => {
      return [course, ...prevCourses];
    });
  };

  const removeHandler = (id) => {
    console.log(courses);
    const newList = courses.filter((item) => item.id !== id);
    setCourses(newList);
    console.log(newList);
  };
  const saveFormDataHandler = () => {
    props.form_submit(courses);
  };
  return (
    <div>
      <Container>
        <Row>
          <Col>
            <MyForm onAddCourse={addCourseHandler} formsubmit={saveFormDataHandler}/>
          </Col>
          <Col>
            <CoursesList items={courses} onRemove={removeHandler}/>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default Home;
