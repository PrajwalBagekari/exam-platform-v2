from fastapi import FastAPI

from ocr_service import OCRService

app = FastAPI()

ocr = OCRService()


@app.get("/health")
def health():

    return {
        "status": "ocr-service-running"
    }


@app.post("/extract")
def extract(image_path: str):

    text = ocr.extract_text(
        image_path
    )

    return {
        "text": text
    }