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
    console.log("LOCATION STATE", location.state);
    console.log("QUESTIONS", questions);
    console.log("QUESTIONS LENGTH", questions?.length);
    console.log("ANSWERS", answers);

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
        <h3>
          Questions Received:
          {questions.length}
        </h3>
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

            const correctAnswer =
              question.correct_answer;

            const isCorrect =
              selectedAnswer &&
              selectedAnswer.toUpperCase() ===
                correctAnswer?.toUpperCase();

            const options = [
              {
                key: "A",
                text: question.option_a,
              },
              {
                key: "B",
                text: question.option_b,
              },
              {
                key: "C",
                text: question.option_c,
              },
              {
                key: "D",
                text: question.option_d,
              },
              ...(question.option_e
                ? [
                    {
                      key: "E",
                      text: question.option_e,
                    },
                  ]
                : []),
            ];

            return (
              <div
                key={question.id || index}
                style={{
                  border: "1px solid #e5e7eb",
                  borderRadius: "12px",
                  padding: "16px",
                  marginBottom: "20px",
                  backgroundColor: "#ffffff",
                }}
              >
                <h3>
                  Question {questionNumber}
                </h3>

                <p>
                  {question.question}
                </p>

                {options.map((option) => {

                  const isSelected =
                    selectedAnswer ===
                    option.key;

                  const isActualAnswer =
                    correctAnswer?.toUpperCase() ===
                    option.key;

                  return (
                    <div
                      key={option.key}
                      style={{
                        padding: "10px",
                        marginBottom: "8px",
                        borderRadius: "8px",

                        border:
                          isActualAnswer
                            ? "2px solid #16a34a"
                            : isSelected
                            ? "2px solid #dc2626"
                            : "1px solid #d1d5db",

                        backgroundColor:
                          isActualAnswer
                            ? "#dcfce7"
                            : isSelected
                            ? "#fee2e2"
                            : "#f9fafb",
                      }}
                    >
                      <strong>
                        {option.key}.
                      </strong>{" "}
                      {option.text}

                      {isSelected &&
                        !isActualAnswer && (
                          <span
                            style={{
                              color: "#dc2626",
                              marginLeft: "10px",
                              fontWeight: "bold",
                            }}
                          >
                            ← Your Answer
                          </span>
                        )}

                      {isActualAnswer && (
                        <span
                          style={{
                            color: "#16a34a",
                            marginLeft: "10px",
                            fontWeight: "bold",
                          }}
                        >
                          ← Correct Answer
                        </span>
                      )}
                    </div>
                  );
                })}

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

                  {correctAnswer?.toUpperCase()}
                  {". "}
                  {getOptionText(
                    question,
                    correctAnswer
                  )}
                </div>

                <div
                  style={{
                    marginTop: "12px",
                    fontWeight: "bold",
                    fontSize: "16px",
                    color:
                      !selectedAnswer
                        ? "#f59e0b"
                        : isCorrect
                        ? "#16a34a"
                        : "#dc2626",
                  }}
                >
                  {!selectedAnswer
                    ? "⏭ Skipped"
                    : isCorrect
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