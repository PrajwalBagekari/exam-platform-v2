import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import SubmitSectionModal from "../components/SubmitSectionModal";
import QuestionPalette from "../components/QuestionPalette";

type Question = {
  id: number;
  question: string;

  description?: string;

  image_path?: string;
  shared_image_path?: string;
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

  useEffect(() => {

    const savedAnswers =
      localStorage.getItem(
        "answers"
      );

    if (savedAnswers) {

      setAnswers(
        JSON.parse(
          savedAnswers
        )
      );

    }

  }, []);

  useEffect(() => {

    localStorage.setItem(
      "answers",
      JSON.stringify(
        answers
      )
    );

  }, [answers]);
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
        },
        }
    );

    };
    useEffect(() => {

    localStorage.setItem(
        "answers",
        JSON.stringify(answers)
    );

    }, [answers]);

  useEffect(() => {

  const loadQuestions = async () => {

      try {

        const response =
          await axios.get(
            `http://pdf2exam.org:8006/exam/${id}/questions`
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
          [...(response.data.questions || [])].sort(
            (a: any, b: any) => {

              const qa = Number(
                a.question.match(/^Q(\d+)/)?.[1] || 0
              );

              const qb = Number(
                b.question.match(/^Q(\d+)/)?.[1] || 0
              );

              return qa - qb;
            }
          );

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
    

  
  

  const currentData =
    questions[currentQuestion - 1];
    console.log(
      "CURRENT QUESTION INDEX:",
      currentQuestion - 1
    );

  console.log(
    "CURRENT QUESTION TEXT:",
    currentData?.question
  );
  console.log(
    "CURRENT DESCRIPTION:",
    currentData?.description
  );

  console.log(
    "CURRENT IMAGE:",
    currentData?.shared_image_path
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

      setQuestionStatusForCurrent(
        "answered"
      );

    } else {

      setQuestionStatusForCurrent(
        "unseen"
      );

    }

    if (currentQuestion < totalQuestions) {

      setCurrentQuestion(
        currentQuestion + 1
      );

    }

  };

 const skipQuestion = () => {

      setQuestionStatusForCurrent(
        "skipped"
      );

      if (currentQuestion < totalQuestions) {

        setCurrentQuestion(
          currentQuestion + 1
        );

      }

    };
  

  const markForReview = () => {

    setQuestionStatusForCurrent(
      "review"
    );

    if (currentQuestion < totalQuestions) {

      setCurrentQuestion(
        currentQuestion + 1
      );

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

  if (loading) {
    return (
      <h1>
        Loading Questions...
      </h1>
    );
  }

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

          <div
              style={{
                whiteSpace: "pre-wrap"
              }}
            >
              <strong>
                {currentData.question}
              </strong>
            </div>

         {currentData.description && (
          <div
            style={{
              marginTop: "10px",
              whiteSpace: "pre-wrap",
              padding: "10px",
              background: "#f5f5f5",
              borderRadius: "6px",
            }}
          >
            {currentData.description}
        </div>
        )}

            {currentData.shared_image_path && (
              <div style={{ marginTop: "15px" }}>
                <img
                  src={currentData.shared_image_path}
                  alt="Question"
                  style={{
                    maxWidth: "100%",
                    border: "1px solid #ccc",
                    borderRadius: "6px",
                  }}
                />
              </div>
      
        )}

          <div>
            <input
              type="radio"
              name="q"
              checked={
                selectedAnswer === "A"
              }
              onChange={() =>
                setAnswers({
                  ...answers,
                  [currentQuestion]: "A",
                })
              }
            />
            {
              currentData.option_a
            }
          </div>

          <div>
            <input
              type="radio"
              name="q"
              checked={
                selectedAnswer === "B"
              }
              onChange={() =>
                setAnswers({
                  ...answers,
                  [currentQuestion]: "B",
                })
              }
            />
            {
              currentData.option_b
            }
          </div>

          <div>
            <input
              type="radio"
              name="q"
              checked={
                selectedAnswer === "C"
              }
              onChange={() =>
                setAnswers({
                ...answers,
                [currentQuestion]: "C",
                })
              }
            />
            {
              currentData.option_c
            }
          </div>

          <div>
            <input
              type="radio"
              name="q"
              checked={
                selectedAnswer === "D"
              }
              onChange={() =>
                setAnswers({
                  ...answers,
                  [currentQuestion]: "D",
                })
              }
            />
            {" "}
            {
              currentData.option_d
            }
          </div>

          {currentData.option_e && (
            <div>
              <input
                type="radio"
                name="q"
                checked={
                  selectedAnswer === "E"
                }
                onChange={() =>
                  setAnswers({
                    ...answers,
                    [currentQuestion]: "E",
                  })
                }
              />
              {" "}
              {
                currentData.option_e
              }
            </div>
          )}

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