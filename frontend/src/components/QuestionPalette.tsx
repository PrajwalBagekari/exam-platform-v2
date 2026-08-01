interface Props {
  currentQuestion: number;
  totalQuestions: number;
  questionStatus: Record<number, string>;
  onSelectQuestion: (
    questionNumber: number
  ) => void;
}

export default function QuestionPalette({
  currentQuestion,
  totalQuestions,
  questionStatus,
  onSelectQuestion,
}: Props) {

  const buttons = [];

  for (
    let i = 1;
    i <= totalQuestions;
    i++
  ) {

    let color = "#d3d3d3";

    if (
      questionStatus[i] === "answered"
    ) {
      color = "green";
    } else if (
      questionStatus[i] === "skipped"
    ) {
      color = "red";
    } else if (
      questionStatus[i] === "review"
    ) {
      color = "orange";
    }

    if (
      currentQuestion === i
    ) {
      color = "#2196f3";
    }

    buttons.push(
      <button
        key={i}
        onClick={() =>
          onSelectQuestion(i)
        }
        style={{
          margin: "5px",
          width: "45px",
          height: "45px",
          border: "none",
          borderRadius: "6px",
          backgroundColor: color,
          color: "white",
          fontWeight: "bold",
          cursor: "pointer",
        }}
      >
        {i}
      </button>
    );
  }

  return (
    <div>

      <h3>
        Questions
      </h3>

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
        }}
      >
        {buttons}
      </div>

      <hr />

      <div>

        <p>
          🔵 Current
        </p>

        <p>
          🟢 Answered
        </p>

        <p>
          🔴 Skipped
        </p>

        <p>
          🟠 Review
        </p>

        <p>
          ⚪ Not Visited
        </p>

      </div>

    </div>
  );
}