from paddleocr import PaddleOCR

ocr = PaddleOCR(
    lang="en",
    device="cpu"
)


class OCRService:

    def __init__(self):

        self.ocr = PaddleOCR(
            lang="en"
        )

    def extract_text(
        self,
        image_path
    ):

        result = self.ocr.predict(
            image_path
        )

        text = []

        for page in result:

            if "rec_texts" in page:

                text.extend(
                    page["rec_texts"]
                )

        return "\n".join(text)