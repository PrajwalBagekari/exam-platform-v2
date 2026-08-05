import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";

export default function ExamSummary() {
  const { id } = useParams();

  const navigate = useNavigate();

  const [professionalTime, setProfessionalTime] =
    useState(60);

  const [exam, setExam] =
    useState<any>(null);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {

    const loadExam =
      async () => {

        try {

          const response =
            await axios.get(
              `https://pdf2exam.org:/exam/${id}/questions`
            );

          setExam({
            totalQuestions:
              response.data.questions.length,
          });

        } catch (error) {

          console.error(error);

        } finally {

          setLoading(false);

        }

      };

    loadExam();

  }, [id]);

  const startExam = () => {

    navigate(
      `/attempt/${id}`
    );

  };

  if (loading) {

    return (
      <h1>
        Loading...
      </h1>
    );

  }

  return (
    <div
      style={{
        padding: "20px",
      }}
    >
      <h1>
        Exam Summary
      </h1>

      <h3>
        Total Questions:{" "}
        {exam?.totalQuestions || 0}
      </h3>

      <hr />

      <h2>
        Sections
      </h2>

      <p>
        General Section :{" "}
        {exam?.totalQuestions || 0}
      </p>

      <hr />

      <h2>
        Timer Settings
      </h2>

      <div>
        <label>
          Exam Duration
          (Minutes)
        </label>

        <br />

        <input
          type="number"
          value={professionalTime}
          onChange={(e) =>
            setProfessionalTime(
              Number(
                e.target.value
              )
            )
          }
        />
      </div>

      <br />

      <button
        onClick={startExam}
      >
        START EXAM
      </button>
    </div>
  );
}