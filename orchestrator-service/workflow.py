import requests


class WorkflowManager:

    def process_pdf(
        self,
        pdf_path
    ):

        result = {}

        # -------------------
        # PDF SERVICE
        # -------------------

        pdf_response = requests.post(
            "https://pdf-service:8001/process",
            params={
                "pdf_path": pdf_path
            }
        )

        result["pdf"] = (
            pdf_response.json()
        )

        # -------------------
        # IMAGE SERVICE
        # -------------------

        image_response = requests.post(
            "https://image-service:8005/render",
            params={
                "pdf_path": pdf_path
            }
        )

        image_data = (
            image_response.json()
        )

        result["images"] = image_data

        # -------------------
        # OCR SERVICE
        # -------------------

        ocr_results = []

        pages = image_data.get(
            "pages",
            []
        )

        for page in pages:

            try:

                response = requests.post(
                    "https://rag-service:8004/extract",
                    params={
                        "image_path": page
                    }
                )

                ocr_results.append(
                    response.json()
                )

            except Exception as ex:

                ocr_results.append(
                    {
                        "error": str(ex)
                    }
                )

        result["ocr"] = (
            ocr_results
        )

        return result