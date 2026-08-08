import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";

export default function ExamDashboard() {
  const { id } = useParams();
  const navigate = useNavigate();

  return (
    <div
      style={{
        minHeight: "100vh",
        background:
          "linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #2563eb 100%)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "30px",
        fontFamily: "Segoe UI, sans-serif",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "1200px",
          background: "rgba(255,255,255,0.95)",
          borderRadius: "24px",
          overflow: "hidden",
          boxShadow: "0 25px 60px rgba(0,0,0,0.25)",
        }}
      >
        <div
          style={{
            background:
              "linear-gradient(135deg, #2563eb, #3b82f6, #60a5fa)",
            padding: "50px",
            color: "white",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexWrap: "wrap",
          }}
        >
          <div>
            <h1
              style={{
                margin: 0,
                fontSize: "42px",
                fontWeight: 700,
              }}
            >
              PDF2EXAM
            </h1>

            <p
              style={{
                marginTop: "10px",
                fontSize: "18px",
                opacity: 0.95,
              }}
            >
              Convert PDFs into Interactive Online Exams
            </p>
          </div>

          <div
            style={{
              fontSize: "80px",
            }}
          >
            ✅
          </div>
        </div>

        <div style={{ padding: "40px" }}>
          <div
            style={{
              background: "#ecfdf5",
              border: "2px solid #22c55e",
              borderRadius: "15px",
              padding: "20px",
              marginBottom: "30px",
            }}
          >
            <h2
              style={{
                color: "#166534",
                margin: 0,
              }}
            >
              Exam Generated Successfully
            </h2>

            <p
              style={{
                marginTop: "10px",
                color: "#15803d",
                fontSize: "18px",
              }}
            >
              Your exam is ready for candidates.
            </p>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit,minmax(220px,1fr))",
              gap: "20px",
              marginBottom: "40px",
            }}
          >
            <div
              style={{
                padding: "25px",
                borderRadius: "18px",
                background: "#eff6ff",
                border: "1px solid #bfdbfe",
              }}
            >
              <h3 style={{ margin: 0, color: "#2563eb" }}>
                Exam ID
              </h3>

              <h1
                style={{
                  margin: "10px 0 0",
                  color: "#1e3a8a",
                }}
              >
                {id}
              </h1>
            </div>

            <div
              style={{
                padding: "25px",
                borderRadius: "18px",
                background: "#fef9c3",
                border: "1px solid #fde047",
              }}
            >
              <h3 style={{ margin: 0 }}>
                Status
              </h3>

              <h1
                style={{
                  margin: "10px 0 0",
                }}
              >
                Ready
              </h1>
            </div>

            <div
              style={{
                padding: "25px",
                borderRadius: "18px",
                background: "#f5f3ff",
                border: "1px solid #c4b5fd",
              }}
            >
              <h3 style={{ margin: 0 }}>
                Platform
              </h3>

              <h1
                style={{
                  margin: "10px 0 0",
                }}
              >
                PDF2EXAM
              </h1>
            </div>
          </div>

          <div
            style={{
              background: "#f8fafc",
              borderRadius: "20px",
              padding: "30px",
              border: "1px solid #e2e8f0",
            }}
          >
            <h2
              style={{
                marginTop: 0,
                color: "#1e293b",
              }}
            >
              Available Actions
            </h2>

            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "15px",
                marginTop: "20px",
              }}
            >
              <button
                onClick={() =>
                  navigate(`/exam/${id}`)
                }
                style={{
                  background: "#2563eb",
                  color: "white",
                  border: "none",
                  padding: "14px 28px",
                  borderRadius: "12px",
                  cursor: "pointer",
                  fontSize: "16px",
                  fontWeight: 600,
                }}
              >
                🚀 Start Exam
              </button>

              <button
                style={{
                  background: "#e2e8f0",
                  color: "#1e293b",
                  border: "none",
                  padding: "14px 28px",
                  borderRadius: "12px",
                  cursor: "pointer",
                  fontSize: "16px",
                  fontWeight: 600,
                }}
              >
                📄 View Questions
              </button>

              <button
                style={{
                  background: "#dcfce7",
                  color: "#166534",
                  border: "none",
                  padding: "14px 28px",
                  borderRadius: "12px",
                  cursor: "pointer",
                  fontSize: "16px",
                  fontWeight: 600,
                }}
              >
                📊 Analytics
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}