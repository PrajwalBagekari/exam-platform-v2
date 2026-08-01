from pdf2docx import Converter
from docx import Document
import fitz
import os

class PDFProcessor:

    def process_pdf(self, pdf_path):

        docx_path = pdf_path.replace(
            ".pdf",
            ".docx"
        )

        cv = Converter(pdf_path)

        cv.convert(docx_path)

        cv.close()

        doc = Document(docx_path)

        for section in doc.sections:

            for p in section.header.paragraphs:
                p.text = ""

            for p in section.footer.paragraphs:
                p.text = ""

        doc.save(docx_path)

        text = []

        for para in doc.paragraphs:

            if para.text.strip():

                text.append(
                    para.text
                )
        

        return {

            "docx": docx_path,

            "text": "\n".join(text)

        }
