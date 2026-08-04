import { useLocation } from "react-router-dom";


export default function Result() {
  const location = useLocation();
    const {
    score = 0,
    totalQuestions = 0,
    attempted = 0,
    skipped = 0,
    notVisited = 0,
    timeLeft = 0,
    } = location.state || {};

    const correct = score;

    const incorrect =
    Math.max(
        attempted - correct,
        0
    );

    const unseen =
    notVisited;

    const accuracy =
    attempted > 0
        ? (
            (correct /
            attempted) *
            100
        ).toFixed(2)
        : "0.00";

    const totalTime = 60;

    const utilizedTime =
    Math.max(
        totalTime -
        Math.floor(
            timeLeft / 60
        ),
        0
    );

    const wastedTime =
    Math.max(
        totalTime -
        utilizedTime,
        0
    );
  const cardStyle = {
    background: "#ffffff",
    borderRadius: "12px",
    padding: "20px",
    boxShadow:
      "0 2px 10px rgba(0,0,0,0.1)",
    textAlign: "center" as const,
  };

  const renderCard = (
    title: string,
    value: string | number
  ) => (
    <div style={cardStyle}>
      <h3>{title}</h3>

      <h2
        style={{
          marginTop: "10px",
        }}
      >
        {value}
      </h2>
    </div>
  );

  return (
    <div
      style={{
        padding: "30px",
        background: "#f4f6f8",
        minHeight: "100vh",
      }}
    >
      <div
        style={{
          width: "100%",
          background: "#e8f5e9",
          color: "#2e7d32",
          padding: "25px",
          borderRadius: "12px",
          textAlign: "center",
          fontSize: "28px",
          fontWeight: "bold",
          marginBottom: "30px",
        }}
      >
        🎉 Congratulations!
        You have successfully
        completed the exam.

        <button
          onClick={() => {
                window.location.href = "/";
            }}
          style={{
            marginTop: "20px",
            padding: "10px 20px",
            background: "#2e7d32",
            color: "#e2e9d9ef",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Upload New Exam
        </button>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(3, 1fr)",
          gap: "20px",
        }}
      >
        {renderCard(
          "Score",
          `${score}/${totalQuestions}`
        )}

        {renderCard(
          "Attempted",
          attempted
        )}

        {renderCard(
          "Correct",
          correct
        )}

        {renderCard(
          "Incorrect",
          incorrect
        )}

        {renderCard(
          "Skipped",
          skipped
        )}

        {renderCard(
          "Unseen",
          unseen
        )}

        {renderCard(
          "Accuracy",
          `${accuracy}%`
        )}

        {renderCard(
          "Total Time",
          `${totalTime} Min`
        )}

        {renderCard(
          "Utilized Time",
          `${utilizedTime} Min`
        )}

        {renderCard(
          "Wasted Time",
          `${wastedTime} Min`
        )}
      </div>

      <div
        style={{
          marginTop: "50px",
          background: "#ffffff",
          padding: "20px",
          borderRadius: "12px",
          boxShadow:
            "0 2px 10px rgba(0,0,0,0.1)",
        }}
      >
        <h1>
          📊 Sectional Analysis
        </h1>
      </div>

      <div
        style={{
          marginTop: "20px",
          marginBottom: "10px",
          fontSize: "22px",
          fontWeight: "bold",
        }}
      >
        General Section
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(3, 1fr)",
          gap: "20px",
        }}
      >
        {renderCard(
          "Score",
          `${score}/${totalQuestions}`
        )}

        {renderCard(
          "Attempted",
          attempted
        )}

        {renderCard(
          "Correct",
          correct
        )}

        {renderCard(
          "Incorrect",
          incorrect
        )}

        {renderCard(
          "Skipped",
          skipped
        )}

        {renderCard(
          "Unseen",
          unseen
        )}

        {renderCard(
          "Accuracy",
          `${accuracy}%`
        )}

        {renderCard(
          "Total Time",
          `${totalTime} Min`
        )}

        {renderCard(
          "Utilized Time",
          `${utilizedTime} Min`
        )}

        {renderCard(
          "Wasted Time",
          `${wastedTime} Min`
        )}
      </div>
    </div>
  );
}