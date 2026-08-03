from fastapi import FastAPI

from pdf_processor import PDFProcessor
from fastapi.staticfiles import StaticFiles

app = FastAPI()
from pathlib import Path

UPLOADS_DIR = (
    Path(__file__).resolve().parent.parent
    / "langgraph-service"
    / "uploads"
)

app.mount(
    "/images",
    StaticFiles(directory=UPLOADS_DIR),
    name="images"
)

processor = PDFProcessor()


@app.get("/health")
def health():

    return {
        "status": "running"
    }


@app.post("/process")
def process(pdf_path: str):

    return processor.process_pdf(
        pdf_path
    )
