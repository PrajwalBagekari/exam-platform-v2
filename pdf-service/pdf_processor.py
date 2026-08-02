from pdf2docx import Converter
from docx import Document
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

        image_dir = docx_path.replace(
            ".docx",
            "_images"
        )

        os.makedirs(
            image_dir,
            exist_ok=True
        )

        image_paths = []

        for rel in doc.part.rels.values():

            if "image" in rel.target_ref:

                image_data = (
                    rel.target_part.blob
                )

                image_name = (
                    f"image_{len(image_paths)+1}.png"
                )

                image_path = os.path.join(
                    image_dir,
                    image_name
                )

                with open(
                    image_path,
                    "wb"
                ) as f:

                    f.write(
                        image_data
                    )

                image_paths.append(
                    image_path
                )

        text = []

        for para in doc.paragraphs:

            if para.text.strip():

                text.append(
                    para.text
                )

        print(
            "\nIMAGES FOUND:"
        )

        print(
            len(image_paths)
        )

        for img in image_paths:

            print(img)
        cleaned_text = "\n".join(text)

        noise_patterns = [
            "adda247.com/defence",
            "www.sscadda.com",
            "www.bankersadda.com",
            "www.adda247.com",
        ]

        for pattern in noise_patterns:

            cleaned_text = cleaned_text.replace(
                pattern,
                ""
            )

        return {

            "docx":
            docx_path,

            "text":
            "\n".join(text),

            "images":
            image_paths

        }