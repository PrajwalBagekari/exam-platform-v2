import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import SubmitSectionModal from "../components/SubmitSectionModal";
import QuestionPalette from "../components/QuestionPalette";

type Question = {
  id: number;
  question: string;
  is_code?: boolean;

  description?: string;
  table_data?: any;

  image_path?: string;

  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  option_e?: string;

  correct_answer?: string;
};
export default function TakeExam() {

  const { id } = useParams();

  const navigate =
    useNavigate();

  const [questions, setQuestions] =
    useState<Question[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [currentQuestion, _setCurrentQuestion] =
    useState(1);

  const setCurrentQuestion = (value: number) => {

    console.log(
      "SET CURRENT QUESTION CALLED:",
      value
    );

  _setCurrentQuestion(value);
};

  const [timeLeft, setTimeLeft] =
    useState(60 * 60);

  const [questionStatus, setQuestionStatus] =
    useState<Record<number, string>>({});

  const [answers, setAnswers] =
    useState<Record<number, string>>({});

  const [showSubmitSection, setShowSubmitSection] =
    useState(false);

  const [examSubmitted, setExamSubmitted] =
    useState(false);

  const totalQuestions =
    questions.length;


  const calculateScore = () => {

        let correct = 0;

        questions.forEach(
            (question, index) => {

            const questionNumber =
                index + 1;

            const userAnswer =
                answers[questionNumber];

            if (
                userAnswer &&
                userAnswer.toLowerCase() ===
                question.correct_answer?.toLowerCase()
            ) {

                correct++;

            }

            }
        );

        return correct;

        };
    const exitExam = () => {

    const confirmExit =
        window.confirm(
        "Are you sure you want to exit the exam? Your score will be calculated immediately."
        );

    if (!confirmExit) {
        return;
    }

    setExamSubmitted(true);

    const score =
        calculateScore();

    navigate(
    "/result",
    {
      state: {
        score,
        totalQuestions,
        attempted,
        skipped,
        review,
        notVisited,
        timeLeft,
        questions,
        answers,
      },
    }
  );
    };


  useEffect(() => {

  const loadQuestions = async () => {

      try {

        const response =
          await axios.get(
            `https://pdf2exam.org/exam/${id}/questions`
          );

        console.log(
          "FIRST 20 QUESTIONS",
          response.data.questions
            .slice(0, 20)
            .map((q: any) =>
              q.question.substring(0, 30)
            )
        );

        const sortedQuestions =
          [...(response.data.questions || [])]
            .map((q: any) => ({
              ...q,
              image_path: q.image_path
                ? q.image_path.replace(/<[^>]*>/g, "")
                : null,
            }))
            .sort((a: any, b: any) => {
              const qa = Number(
                a.question.match(/^Q(\d+)/)?.[1] || 0
              );

              const qb = Number(
                b.question.match(/^Q(\d+)/)?.[1] || 0
              );

              return qa - qb;
            });

        console.log(
          "SORTED QUESTION NUMBERS",
          sortedQuestions.map((q: any) =>
            q.question.match(/^Q(\d+)/)?.[1]
          )
        );

        setQuestions(
                  sortedQuestions
                );
                console.log(
          "FIRST QUESTION:",
          sortedQuestions[0]?.question
        );

        console.log(
          "SECOND QUESTION:",
          sortedQuestions[1]?.question
        );

        console.log(
          "THIRD QUESTION:",
          sortedQuestions[2]?.question
        );

      } catch (error) {

        console.error(error);

      } finally {

        setLoading(false);

      }

    };
    loadQuestions();
    
    const timer = setInterval(() => {

        setTimeLeft((prev) => {

        if (
            prev <= 0 &&
            !examSubmitted
        ) {

            setExamSubmitted(true);

            clearInterval(timer);

            const score =
            calculateScore();

            navigate(
            "/result",
            {
                state: {
                score,
                totalQuestions,
                },
            }
            );

            return 0;
        }

        return prev - 1;

        });

    }, 1000);

    return () =>
        clearInterval(timer);

    }, [
    navigate,
    totalQuestions,
    examSubmitted
    ]);
  
  if (loading) {
    return (
      <h1>
        Loading Questions...
      </h1>
    );
  }
  
  const currentData =
   questions?.[currentQuestion - 1];


  if (!currentData) {
    return <h1>Loading Questions...</h1>;
  }

  let parsedTableData = currentData?.table_data;

  if (typeof parsedTableData === "string") {
    try {
      parsedTableData = JSON.parse(parsedTableData);
    } catch (e) {
      console.error(
        "TABLE PARSE ERROR:",
        e
      );
      parsedTableData = null;
    }
  }

  console.log(
    "PARSED TABLE DATA:",
    parsedTableData
  );

  if (!questions.length) {
    console.log(
      "FIRST 10 QUESTIONS",
      questions.slice(0, 10).map(
        q => q.question
      )
    );
    
    return (
      <h1>
        No Questions Found
      </h1>
    );
  }
    

  
  

  

  console.log(
    "CURRENT QUESTION TEXT:",
    currentData?.question
  );
  console.log(
    "CURRENT TABLE:",
    currentData?.table_data
  );
  console.log(
    "TABLE TYPE:",
    typeof currentData?.table_data
  );

  console.log(
    "TABLE VALUE:",
    currentData?.table_data
  );

  console.log(
    "PARSED TABLE:",
    parsedTableData
  );
  console.log(
    "CURRENT DESCRIPTION:",
    currentData?.description
  );
  console.log(
  "IS_CODE:",
  currentData?.is_code
);

  console.log(
    "CURRENT DATA:",
    currentData
  );

  console.log(
    "CURRENT IMAGE:",
    currentData?.image_path
  );

  const selectedAnswer =
    answers[currentQuestion];

  const minutes =
    Math.floor(timeLeft / 60);

  const seconds =
    timeLeft % 60;

    const setQuestionStatusForCurrent = (status: string) => {
      const keyValuePair = { [currentQuestion]: status };
      setQuestionStatus((prev) => ({
        ...prev,
        ...keyValuePair,
      }));
    };

    const saveAndNext = () => {
      if (answers[currentQuestion]) {
        setQuestionStatusForCurrent("answered");
      }

      if (currentQuestion < totalQuestions) {
        setCurrentQuestion(currentQuestion + 1);
      }
    };

    const skipQuestion = () => {
      setQuestionStatusForCurrent("skipped");

      if (currentQuestion < totalQuestions) {
        setCurrentQuestion(currentQuestion + 1);
      }
    };

    const markForReview = () => {
      setQuestionStatusForCurrent("review");

      if (currentQuestion < totalQuestions) {
        setCurrentQuestion(currentQuestion + 1);
      }
    };

  const attempted =
    Object.values(
      questionStatus
    ).filter(
      (status) =>
        status === "answered"
    ).length;

  const skipped =
    Object.values(
      questionStatus
    ).filter(
      (status) =>
        status === "skipped"
    ).length;

  const review =
    Object.values(
      questionStatus
    ).filter(
      (status) =>
        status === "review"
    ).length;

  const notVisited =
    totalQuestions -
    attempted -
    skipped -
    review;

  const previousQuestion = () => {

    if (currentQuestion > 1) {

        setCurrentQuestion(
        currentQuestion - 1
        );

    }

    };
    
    


  return (
    <>
      <div
        style={{
          display: "flex",
        }}
      >
        <div
          style={{
            flex: 3,
            padding: "20px",
          }}
        >
          <h1>
            Exam Started
          </h1>

          <h2>
            Exam ID: {id}
          </h2>

          <h2
            style={{
              color: "red",
            }}
          >
            Time Remaining{" "}
            {minutes}:
            {String(seconds).padStart(
              2,
              "0"
            )}
          </h2>

          <hr />

          <h3>
            Question{" "}
            {currentQuestion}
            {" / "}
            {totalQuestions}
          </h3>

          {currentData.is_code ? (
            <div
              style={{
                marginTop: "15px",
                marginBottom: "15px",
              }}
            >
              <pre
                style={{
                  whiteSpace: "pre-wrap",
                  wordBreak: "break-word",
                  overflowX: "auto",
                  background: "#f8fafc",
                  padding: "20px",
                  borderRadius: "8px",
                  border: "1px solid #e2e8f0",
                  fontFamily: "Consolas, Monaco, 'Courier New', monospace",
                  fontSize: "14px",
                  lineHeight: "1.6",
                  margin: 0,
                }}
              >
                {currentData.question
                  ?.replace(/\s*#include/g, "\n#include")
                  ?.replace(/\s*using namespace/g, "\n\nusing namespace")
                  ?.replace(/\s*int main/g, "\n\nint main")
                  ?.replace(/\s*void /g, "\n\nvoid ")
                }
              </pre>
            </div>
          ) : (
            <p>
              <strong>{currentData.question}</strong>
            </p>
          )}

          {currentData?.description && (
            <div
              style={{
                marginTop: "15px",
                whiteSpace: "pre-wrap",
                padding: "15px",
                background: "#f5f5f5",
                borderRadius: "6px",
                lineHeight: "1.6",
              }}
            >
              {
                currentData.description.replace(
                  /\[\[IMAGE:.*?\]\]/g,
                  ""
                )
              }
            </div>
          )}
          

          {currentData.image_path && (
            <div style={{ marginTop: "15px" }}>
              <img
                src={currentData.image_path}
                alt="Question"
                style={{
                  maxWidth: "100%",
                  border: "1px solid #ccc",
                  borderRadius: "6px",
                }}
              />
            </div>
          )}
          
          {parsedTableData &&
            Array.isArray(parsedTableData) && (
              <table
                style={{
                  width: "100%",
                  borderCollapse: "collapse",
                  marginTop: "15px",
                }}
              >
                <tbody>
                  {parsedTableData.map(
                    (row: any, rowIndex: number) => (
                      <tr key={rowIndex}>
                        {row.map(
                          (cell: any, cellIndex: number) => (
                            <td
                              key={cellIndex}
                              style={{
                                border: "1px solid #ccc",
                                padding: "8px",
                              }}
                            >
                              {cell}
                            </td>
                          )
                        )}
                      </tr>
                    )
                  )}
                </tbody>
              </table>
            )}
          {[
              { key: "A", text: currentData.option_a },
              { key: "B", text: currentData.option_b },
              { key: "C", text: currentData.option_c },
              { key: "D", text: currentData.option_d },
              ...(currentData.option_e
                ? [{ key: "E", text: currentData.option_e }]
                : []),
            ].map((option) => (
              <label
                key={option.key}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "12px",
                  padding: "14px",
                  marginBottom: "12px",
                  border:
                    selectedAnswer === option.key
                      ? "2px solid #2563eb"
                      : "1px solid #d1d5db",
                  borderRadius: "10px",
                  backgroundColor:
                    selectedAnswer === option.key
                      ? "#eff6ff"
                      : "#ffffff",
                  cursor: "pointer",
                }}
              >
                <input
                  type="radio"
                  name={`q-${currentQuestion}`}
                  checked={selectedAnswer === option.key}
                  onChange={() =>
                        setAnswers({
                          ...answers,
                          [currentQuestion]: option.key
                        })
                      }
                />

                <strong
                  style={{
                    color: "#2563eb",
                    minWidth: "24px",
                  }}
                >
                  {option.key}.
                </strong>

                <span>
                  {option.text}
                </span>
              </label>
            ))}

          <br />
          <button
            onClick={previousQuestion}
            >
            Previous
            </button>

            {" "}

          <button
            onClick={
              saveAndNext
            }
          >
            Save & Next
          </button>

          {" "}

          <button
            onClick={
              skipQuestion
            }
          >
            Skip
          </button>

          {" "}

          <button
            onClick={
              markForReview
            }
          >
            Mark For Review
          </button>

          {" "}

          <button
            onClick={() =>
              setShowSubmitSection(
                true
              )
            }
          >
            Submit Section
          </button>
          {" "}

            <button
            onClick={exitExam}
            style={{
                backgroundColor: "red",
                color: "white",
            }}
            >
            Exit Exam
            </button>
        </div>

        <div
          style={{
            flex: 1,
            borderLeft:
              "1px solid black",
            padding: "20px",
          }}
        >
          <QuestionPalette
            currentQuestion={
              currentQuestion
            }
            totalQuestions={
              totalQuestions
            }
            questionStatus={
              questionStatus
            }
            onSelectQuestion={
              setCurrentQuestion
            }
          />
        </div>
      </div>

      {showSubmitSection && (
        <SubmitSectionModal
        attempted={attempted}
        skipped={skipped}
        review={review}
        notVisited={notVisited}
        onClose={() =>
            setShowSubmitSection(
                false
                )
            }
            onSubmit={() => {

            const score =
                calculateScore();

            navigate(
  "/result",
  {
    state: {
      score,
      totalQuestions,
      attempted,
      skipped,
      review,
      notVisited,
      timeLeft,
    },
  }
);

            }}
        />
      )}
    </>
  );
}