import {
  useParams
} from "react-router-dom";

export default function ExamDashboard() {

  const { id } =
    useParams();

  return (

    <div>

      <h1>
        Exam Dashboard
      </h1>

      <h2>
        Exam ID: {id}
      </h2>

      <p>
        Generated Successfully
      </p>

    </div>

  );

}