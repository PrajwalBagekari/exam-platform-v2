from fastapi import FastAPI

from models import PDFRequest

from workflow import (
    WorkflowManager
)

app = FastAPI()

workflow = WorkflowManager()


@app.get("/")
def root():

    return {

        "service":
        "orchestrator-service",

        "status":
        "running"

    }


@app.get("/health")
def health():

    return {

        "status":
        "orchestrator-running"

    }


@app.post("/process")
def process(
    request: PDFRequest
):

    return workflow.process_pdf(

        request.pdf_path

    )