import fitz
import os
import shutil


class ImageService:

    def render_pdf(
        self,
        pdf_path
    ):

        output_dir = "rendered_pages"

        # Remove old rendered pages
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

        os.makedirs(
            output_dir,
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
                f"{output_dir}/page_{page_num}.png"
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