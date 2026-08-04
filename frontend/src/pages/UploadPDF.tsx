import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function UploadPDF() {

  const [uploading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const navigate = useNavigate();

  const uploadPdf = async () => {
    try {
      if (!file) {
        alert("Select a PDF file");
        return;
      }

      const formData = new FormData();

      formData.append(
        "file",
        file
      );

      const response = await fetch(
        "http://127.0.0.1:8008/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      console.log("Response:", data);

      if (data.exam?.exam_id) {
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
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Exam Platform V2</h1>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => {
          if (
            e.target.files &&
            e.target.files.length > 0
          ) {
            setFile(
              e.target.files[0]
            );
          }
        }}
      />

      <br />
      <br />

      <button
      onClick={uploadPdf}
      disabled={uploading}
      style={{
        opacity: uploading ? 0.6 : 1,
        cursor: uploading
          ? "not-allowed"
          : "pointer",
      }}
    >
      {uploading
        ? "Uploading..."
        : "Upload PDF"}
    </button>
    </div>
  );
}
