import re


class QuestionExtractor:

    def extract_questions(
        self,
        text
    ):

        pattern = (
            r"(Q\\d+\\..*?)"
            r"(?=Q\\d+\\.|$)"
        )

        blocks = re.findall(
            pattern,
            text,
            re.DOTALL
        )

        questions = []

        for block in blocks:

            questions.append(
                {
                    "question":
                    block
                }
            )

        return questions