import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function UploadPDF() {
  const [uploading, setUploading] =
    useState(false);

  const [file, setFile] =
    useState<File | null>(null);

  const navigate = useNavigate();

  const uploadPdf = async () => {
    try {
      if (!file) {
        alert("Please select a PDF file");
        return;
      }

      setUploading(true);

      const formData =
        new FormData();

      formData.append(
        "file",
        file
      );

      const response = await fetch(
        "https://pdf2exam.org/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const responseText =
        await response.text();

      console.log(
        "Server Response:",
        responseText
      );

      if (!response.ok) {
        throw new Error(
          responseText
        );
      }

      const data =
        JSON.parse(responseText);

      console.log(
        "Response:",
        data
      );

      if (
        data.exam?.exam_id
      ) {
        navigate(
          `/exam/${data.exam.exam_id}`
        );
      } else {
        alert(
          "Exam created but no exam_id returned."
        );
      }
    } catch (error) {
      console.error(error);

      alert(
        "Failed to upload PDF."
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background:
          "linear-gradient(135deg,#0f172a,#1e3a8a,#2563eb)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "30px",
        fontFamily:
          "Segoe UI, sans-serif",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "1000px",
          background: "#fff",
          borderRadius: "24px",
          overflow: "hidden",
          boxShadow:
            "0 25px 60px rgba(0,0,0,.25)",
          display: "grid",
          gridTemplateColumns:
            "1fr 1fr",
        }}
      >
        <div
          style={{
            background:
              "linear-gradient(135deg,#2563eb,#3b82f6)",
            color: "white",
            padding: "50px",
            display: "flex",
            flexDirection:
              "column",
            justifyContent:
              "center",
          }}
        >
          <h1
            style={{
              fontSize: "42px",
              margin: 0,
            }}
          >
            AI Powered
          </h1>

          <h2
            style={{
              fontSize: "34px",
              marginTop: "10px",
            }}
          >
            PDF to Exam
          </h2>

          <p
            style={{
              fontSize: "18px",
              lineHeight: 1.7,
              opacity: 0.95,
            }}
          >
            Upload your PDF
            and instantly
            convert it into a
            fully interactive
            online examination
            with questions,
            images, tables,
            timer, answer
            tracking and
            result generation.
          </p>

          <div
            style={{
              fontSize: "90px",
              marginTop: "20px",
            }}
          >
            📚
          </div>
        </div>

        <div
          style={{
            padding: "50px",
            display: "flex",
            flexDirection:
              "column",
            justifyContent:
              "center",
          }}
        >
          <h2
            style={{
              color: "#1e293b",
              marginBottom:
                "10px",
            }}
          >
            Upload Question
            Paper
          </h2>

          <p
            style={{
              color: "#64748b",
              marginBottom:
                "30px",
            }}
          >
            Select a PDF file
            to generate your
            exam automatically.
          </p>

          <div
            style={{
              border:
                "2px dashed #93c5fd",
              borderRadius:
                "14px",
              padding: "40px",
              textAlign:
                "center",
              background:
                "#eff6ff",
            }}
          >
            <div
              style={{
                fontSize: "52px",
                marginBottom:
                  "15px",
              }}
            >
              📄
            </div>

            <input
              type="file"
              accept=".pdf"
              onChange={(e) => {
                if (
                  e.target
                    .files &&
                  e.target
                    .files
                    .length > 0
                ) {
                  setFile(
                    e.target
                      .files[0]
                  );
                }
              }}
              style={{
                width: "100%",
              }}
            />

            {file && (
              <p
                style={{
                  marginTop:
                    "15px",
                  color:
                    "#2563eb",
                  fontWeight:
                    "bold",
                }}
              >
                {file.name}
              </p>
            )}
          </div>

          <button
            onClick={
              uploadPdf
            }
            disabled={
              uploading
            }
            style={{
              marginTop:
                "30px",
              background:
                uploading
                  ? "#94a3b8"
                  : "#2563eb",
              color: "white",
              border: "none",
              borderRadius:
                "12px",
              padding:
                "16px",
              fontSize:
                "18px",
              fontWeight:
                "bold",
              cursor:
                uploading
                  ? "not-allowed"
                  : "pointer",
              transition:
                "0.3s",
            }}
          >
            {uploading
              ? "⏳ Uploading PDF..."
              : "🚀 Generate Exam"}
          </button>
        </div>
      </div>
    </div>
  );
}
