interface Props {
  attempted: number;
  skipped: number;
  review: number;
  notVisited: number;
  onClose: () => void;
  onSubmit: () => void;
}

export default function SubmitSectionModal({
  attempted,
  skipped,
  review,
  notVisited,
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
          padding: "20px",
          borderRadius: "10px",
          minWidth: "350px",
        }}
      >
        <h2>Submit Section</h2>

        <p>Attempted: {attempted}</p>
        <p>Skipped: {skipped}</p>
        <p>Review: {review}</p>
        <p>Not Visited: {notVisited}</p>

        <br />

        <button onClick={onClose}>
          Cancel
        </button>

        {" "}

        <button onClick={onSubmit}>
          Submit Section
        </button>
      </div>
    </div>
  );
}