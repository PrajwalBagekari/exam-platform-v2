from fastapi import FastAPI
from image_service import ImageService

app = FastAPI()

service = ImageService()


@app.get("/")
def root():

    return {
        "service": "image-service",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "image-service-running"
    }


@app.post("/render")
def render(pdf_path: str):

    pages = service.render_pdf(
        pdf_path
    )

    return {
        "total_pages": len(pages),
        "pages": pages
    }

@app.post("/render")
def render(pdf_path: str):

    print("=" * 50)
    print("PDF PATH RECEIVED:")
    print(pdf_path)
    print("=" * 50)

    return {
        "pages": service.render_pdf(pdf_path)
    }
