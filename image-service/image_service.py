import fitz
import os


class ImageService:

    def render_pdf(
        self,
        pdf_path
    ):

        os.makedirs(
            "rendered_pages",
            exist_ok=True
        )

        doc = fitz.open(pdf_path)

        rendered_pages = []

        for page_num in range(len(doc)):

            page = doc[page_num]

            pix = page.get_pixmap(
                matrix=fitz.Matrix(2, 2)
            )

            output_path = os.path.abspath(
                f"rendered_pages/page_{page_num}.png"
            )

            pix.save(
                output_path
            )

            rendered_pages.append(
                output_path
            )

            print(
                f"Generated: {output_path}"
            )

        doc.close()

        return rendered_pages