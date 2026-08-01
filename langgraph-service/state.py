from typing import TypedDict


class ExamState(TypedDict):

    pdf_path: str

    pdf_data: dict

    image_data: dict

    ocr_data: dict

    questions: dict

    rag_data: dict

    exam_data: dict