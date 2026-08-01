import { useLocation } from "react-router-dom";

export default function Result() {

  const location =
    useLocation();

  const {
    score,
    totalQuestions,
  } = location.state;

  const percentage =
    (
      score /
      totalQuestions
    ) * 100;

  return (
    <div
      style={{
        padding: "20px",
      }}
    >
      <h1>
        Exam Result
      </h1>

      <h2>
        Score:
        {score}
        /
        {totalQuestions}
      </h2>

      <h2>
        Percentage:
        {percentage.toFixed(2)}%
      </h2>
    </div>
  );
}