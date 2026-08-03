from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

from fastapi.middleware.cors import (
    CORSMiddleware
)

from workflow import graph

import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://pdf2exam.org"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():

    return {
        "service": "langgraph-service",
        "status": "running"
    }


@app.post("/process")
def process(
    pdf_path: str
):

    state = {
        "pdf_path": pdf_path,
        "pdf_data": {},
        "image_data": {},
        "ocr_data": [],
        "questions": [],
        "rag_data": {},
        "exam_data": {}
    }

    return graph.invoke(
        state
    )


@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    file_path = os.path.abspath(
        os.path.join(
            "uploads",
            file.filename
        )
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    state = {
        "pdf_path": file_path,
        "pdf_data": {},
        "image_data": {},
        "ocr_data": [],
        "questions": [],
        "rag_data": {},
        "exam_data": {}
    }

    print("UPLOADED FILE SAVED TO:")
    print(file_path)

    print("FILE PATH:")
    print(file_path)

    result = graph.invoke(
        state
    )

    return {
        "message":
        "File uploaded successfully",

        "exam":
        result["exam_data"]
    }