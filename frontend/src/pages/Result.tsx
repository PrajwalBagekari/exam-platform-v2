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
    questions = [],
    answers = {},
    } = location.state || {};

    const correct = score;

    const incorrect =
    Math.max(
        attempted - correct,
        0
    );
    const getOptionText = (
      question: any,
      answer?: string
    ) => {
      switch (answer?.toUpperCase()) {
        case "A":
          return question.option_a;

        case "B":
          return question.option_b;

        case "C":
          return question.option_c;

        case "D":
          return question.option_d;

        case "E":
          return question.option_e;

        default:
          return "Not Answered";
      }
    };

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
  const candidateName =
    localStorage.getItem(
      "candidateName"
    );

  const candidateEmail =
    localStorage.getItem(
      "candidateEmail"
    );
  
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
  const sectionStats = questions.reduce(
    (acc: any, question: any, index: number) => {
      const section =
        question.section || "General";

      if (!acc[section]) {
        acc[section] = {
          total: 0,
          attempted: 0,
          correct: 0,
          incorrect: 0,
        };
      }

      acc[section].total++;

      const userAnswer =
        answers[index + 1];

      if (userAnswer) {
        acc[section].attempted++;

        if (
          userAnswer.toLowerCase() ===
          question.correct_answer?.toLowerCase()
        ) {
          acc[section].correct++;
        } else {
          acc[section].incorrect++;
        }
      }

      return acc;
    },
    {}
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
      <h3>
        Name: {candidateName}
      </h3>

      <h3>
        Email: {candidateEmail}
      </h3>
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

      {Object.entries(sectionStats).map(
  ([sectionName, stats]: any) => {
    const accuracy =
      stats.attempted > 0
        ? (
            (stats.correct /
              stats.attempted) *
            100
          ).toFixed(2)
        : "0.00";

    return (
      <div key={sectionName}>
        <div
          style={{
            marginTop: "20px",
            marginBottom: "10px",
            fontSize: "22px",
            fontWeight: "bold",
          }}
        >
          {sectionName}
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
            `${stats.correct}/${stats.total}`
          )}

          {renderCard(
            "Attempted",
            stats.attempted
          )}

          {renderCard(
            "Correct",
            stats.correct
          )}

          {renderCard(
            "Incorrect",
            stats.incorrect
          )}

          {renderCard(
            "Total Questions",
            stats.total
          )}

          {renderCard(
            "Accuracy",
            `${accuracy}%`
          )}
        </div>
      </div>
    );
  }
)}

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
          📝 Question Review
        </h1>

        {questions.map(
          (
            question: any,
            index: number
          ) => {

            const questionNumber =
              index + 1;

            const selectedAnswer =
              answers[questionNumber];

            const isCorrect =
              selectedAnswer?.toLowerCase() ===
              question.correct_answer?.toLowerCase();

            return (
              <div
                key={question.id}
                style={{
                  border:
                    "1px solid #e5e7eb",
                  borderRadius: "12px",
                  padding: "16px",
                  marginBottom: "16px",
                  backgroundColor:
                    "#ffffff",
                }}
              >
                <h3>
                  Question {questionNumber}
                </h3>

                <p>
                  {question.question}
                </p>

                <div
                  style={{
                    marginTop: "12px",
                    padding: "10px",
                    background: "#f8fafc",
                    borderRadius: "8px",
                  }}
                >
                  <strong>
                    Your Answer:
                  </strong>

                  <br />

                  {selectedAnswer
                    ? `${selectedAnswer}. ${getOptionText(
                        question,
                        selectedAnswer
                      )}`
                    : "Not Answered"}
                </div>

                <div
                  style={{
                    marginTop: "12px",
                    padding: "10px",
                    background: "#f8fafc",
                    borderRadius: "8px",
                  }}
                >
                  <strong>
                    Correct Answer:
                  </strong>

                  <br />

                  {question.correct_answer?.toUpperCase()}
                  {". "}
                  {getOptionText(
                    question,
                    question.correct_answer
                  )}
                </div>

                <div
                  style={{
                    marginTop: "12px",
                    fontWeight: "bold",
                    color: isCorrect
                      ? "#16a34a"
                      : "#dc2626",
                  }}
                >
                  {isCorrect
                    ? "✅ Correct"
                    : "❌ Incorrect"}
                </div>
              </div>
            );
          }
        )}
      </div>
    </div>
    
  );
}