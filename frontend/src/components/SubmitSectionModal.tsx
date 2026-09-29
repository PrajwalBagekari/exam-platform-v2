interface Props {
  attempted: number;
  skipped: number;
  review: number;
  notVisited: number;

  currentSectionName: string;
  nextSectionName?: string;
  isLastSection: boolean;

  onClose: () => void;
  onSubmit: () => void;
}

export default function SubmitSectionModal({
  attempted,
  skipped,
  review,
  notVisited,

  currentSectionName,
  nextSectionName,
  isLastSection,

  onClose,
  onSubmit,
}: Props) {
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(0,0,0,0.5)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          background: "white",
          padding: "25px",
          borderRadius: "10px",
          minWidth: "400px",
        }}
      >
        <h2>
          {currentSectionName} Completed
        </h2>

        <div>
          <p>
            <strong>Attempted:</strong>{" "}
            {attempted}
          </p>

          <p>
            <strong>Skipped:</strong>{" "}
            {skipped}
          </p>

          <p>
            <strong>Review:</strong>{" "}
            {review}
          </p>

          <p>
            <strong>Not Visited:</strong>{" "}
            {notVisited}
          </p>
        </div>

        <br />

        {isLastSection ? (
          <h3>
            Submit Entire Exam?
          </h3>
        ) : (
          <h3>
            Proceed To{" "}
            {nextSectionName} ?
          </h3>
        )}

        <br />

        <button onClick={onClose}>
          Cancel
        </button>

        {" "}

        <button onClick={onSubmit}>
          {isLastSection
            ? "Submit Exam"
            : "Start Next Section"}
        </button>
      </div>
    </div>
  );
}