import "./ScheduleList.css";
import axios from "axios";

const ScheduleItem = (props) => {
  const clickHandler = () => {
    axios.get(`http://127.0.0.1:8000/api/dailyschedule/${props.id}`)
    .then((response) => {
      console.log(response);
      props.onView(response.data[0], response.data[1]);
    });
  };
  return (
    <tr>
      {props.schedule.map((section) => (
        <td>{section}</td>
      ))}
      <td>
        <button
          className="bg-gray-700 text-white form-button transition ease-in-out delay-150 hover:scale-105 duration-300"
          onClick={clickHandler}
        >
          View
        </button>
      </td>
    </tr>
  );
};

export default ScheduleItem;
