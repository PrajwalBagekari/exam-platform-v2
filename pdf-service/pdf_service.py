from pdf2docx import Converter
from docx import Document
from pathlib import Path


def process_pdf(pdf_path):

    pdf_path = Path(pdf_path)

    docx_path = pdf_path.with_suffix(".docx")

    cv = Converter(str(pdf_path))

    cv.convert(str(docx_path))

    cv.close()

    doc = Document(str(docx_path))

    for section in doc.sections:

        header = section.header

        footer = section.footer

        for paragraph in header.paragraphs:
            paragraph.text = ""

        for paragraph in footer.paragraphs:
            paragraph.text = ""

    doc.save(str(docx_path))

    extracted_text = []

    doc = Document(str(docx_path))

    for para in doc.paragraphs:

        text = para.text.strip()

        if text:

            extracted_text.append(text)

    return {
        "pdf_file": str(pdf_path),
        "docx_file": str(docx_path),
        "text": "\n".join(extracted_text)
    }