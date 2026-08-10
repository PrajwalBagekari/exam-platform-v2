import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";

export default function ExamSummary() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [exam, setExam] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const [userName, setUserName] = useState("");
  const [email, setEmail] = useState("");

  useEffect(() => {
    const loadExam = async () => {
      try {
        const response = await axios.get(
          `https://pdf2exam.org/exam/${id}/questions`
        );

        const totalQuestions =
          response.data.questions.length;

        setExam({
          totalQuestions,
          totalTime: totalQuestions,
        });
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    loadExam();
  }, [id]);

 const startExam = () => {
    console.log("START EXAM CLICKED");

    if (!userName.trim()) {
      alert("Please enter your name");
      return;
    }

    if (!email.trim()) {
      alert("Please enter your Email ID");
      return;
    }

    navigate(`/attempt/${id}`);
  };

  if (loading) {
    return (
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontSize: "24px",
          fontWeight: 600,
        }}
      >
        Loading Exam...
      </div>
    );
  }

  const sectionTime =
    exam?.totalTime ?? 0;

  return (
    <div
      style={{
        minHeight: "100vh",
        background:
          "linear-gradient(135deg,#0f172a,#1e3a8a,#2563eb)",
        padding: "40px",
        fontFamily: "Segoe UI, sans-serif",
      }}
    >
      <div
        style={{
          maxWidth: "1200px",
          margin: "0 auto",
          background: "#fff",
          borderRadius: "25px",
          overflow: "hidden",
          boxShadow:
            "0 25px 60px rgba(0,0,0,.25)",
        }}
      >
        <div
          style={{
            background:
              "linear-gradient(135deg,#2563eb,#3b82f6)",
            color: "#fff",
            padding: "50px",
            display: "flex",
            justifyContent:
              "space-between",
            alignItems: "center",
            flexWrap: "wrap",
            gap: "25px",
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
                marginTop: "12px",
                fontSize: "18px",
              }}
            >
              Exam Ready For Launch
            </p>
          </div>

          <img
            src="https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=900"
            alt="Exam"
            style={{
              width: "280px",
              height: "180px",
              objectFit: "cover",
              borderRadius: "15px",
              boxShadow: "0 10px 25px rgba(0,0,0,.2)",
            }}
          />
          
        </div>

        <div
          style={{
            padding: "40px",
          }}
        >
          <div
            style={{
              marginBottom: "35px",
            }}
          >
            <h2
              style={{
                color: "#1e293b",
              }}
            >
              Candidate Details
            </h2>

            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "repeat(auto-fit,minmax(280px,1fr))",
                gap: "20px",
              }}
            >
              <input
                type="text"
                placeholder="Enter Full Name"
                value={userName}
                onChange={(e) =>
                  setUserName(
                    e.target.value
                  )
                }
                style={{
                  padding: "14px",
                  border:
                    "1px solid #dbeafe",
                  borderRadius:
                    "10px",
                }}
              />

              <input
                type="email"
                placeholder="Enter Email ID"
                value={email}
                onChange={(e) =>
                  setEmail(
                    e.target.value
                  )
                }
                style={{
                  padding: "14px",
                  border:
                    "1px solid #dbeafe",
                  borderRadius:
                    "10px",
                }}
              />
            </div>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit,minmax(220px,1fr))",
              gap: "20px",
              marginBottom: "35px",
            }}
          >
            <div
              style={{
                background:
                  "#eff6ff",
                padding: "25px",
                borderRadius:
                  "16px",
              }}
            >
              <h4>Exam ID</h4>
              <h2>{id}</h2>
            </div>

            <div
              style={{
                background:
                  "#ecfdf5",
                padding: "25px",
                borderRadius:
                  "16px",
              }}
            >
              <h4>Total Questions</h4>
              <h2>
                {
                  exam?.totalQuestions
                }
              </h2>
            </div>

            <div
              style={{
                background:
                  "#fef3c7",
                padding: "25px",
                borderRadius:
                  "16px",
              }}
            >
              <h4>Total Duration</h4>
              <h2>
                {
                  exam?.totalTime
                }{" "}
                Min
              </h2>
            </div>

            <div
              style={{
                background:
                  "#ede9fe",
                padding: "25px",
                borderRadius:
                  "16px",
              }}
            >
              <h4>Status</h4>
              <h2>Ready</h2>
            </div>
          </div>

          <div
            style={{
              background:
                "#f8fafc",
              padding: "30px",
              borderRadius:
                "18px",
              marginBottom:
                "30px",
            }}
          >
            <h2>
              Exam Sections
            </h2>

            <table
              style={{
                width: "100%",
                borderCollapse:
                  "collapse",
                marginTop: "20px",
              }}
            >
              <thead>
                <tr
                  style={{
                    background:
                      "#2563eb",
                    color:
                      "white",
                  }}
                >
                  <th
                    style={{
                      padding:
                        "15px",
                    }}
                  >
                    Section
                  </th>

                  <th>
                    Questions
                  </th>

                  <th>
                    Time
                  </th>
                </tr>
              </thead>

              <tbody>
                <tr>
                  <td
                    style={{
                      textAlign:
                        "center",
                      padding:
                        "15px",
                    }}
                  >
                    General
                    Section
                  </td>

                  <td
                    style={{
                      textAlign:
                        "center",
                    }}
                  >
                    {
                      exam?.totalQuestions
                    }
                  </td>

                  <td
                    style={{
                      textAlign:
                        "center",
                    }}
                  >
                    {
                      sectionTime
                    }{" "}
                    Minutes
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div
            style={{
              background:
                "#eef2ff",
              padding: "25px",
              borderRadius:
                "18px",
            }}
          >
            <h2>
              Instructions
            </h2>

            <ul>
              <li>
                Each question
                carries equal
                marks.
              </li>

              <li>
                Total Exam Time
                equals Total
                Number of
                Questions
                (Minutes).
              </li>

              <li>
                Do not refresh
                the browser
                during the exam.
              </li>

              <li>
                Submit before
                the timer
                expires.
              </li>
            </ul>
          </div>

          <div
            style={{
              textAlign: "center",
              marginTop: "35px",
            }}
          >
            <button
              onClick={startExam}
              style={{
                background:
                  "#2563eb",
                color: "white",
                border: "none",
                padding:
                  "16px 40px",
                borderRadius:
                  "12px",
                cursor:
                  "pointer",
                fontSize:
                  "18px",
                fontWeight:
                  "bold",
              }}
            >
              🚀 START EXAM
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}