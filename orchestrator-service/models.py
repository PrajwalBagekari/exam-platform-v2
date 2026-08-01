from pydantic import BaseModel


class PDFRequest(BaseModel):

    pdf_path: str