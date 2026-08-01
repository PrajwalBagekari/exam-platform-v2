import re


def extract_questions(text: str):

    questions = []

    pattern = r"(Q\d+\..*?)(?=Q\d+\.|$)"

    blocks = re.findall(
        pattern,
        text,
        flags=re.DOTALL
    )
    print("TOTAL BLOCKS:")
    print(len(blocks))

    for block in blocks:

        question_match = re.search(
            r"^(Q\d+\..*?)(?=\(a\))",
            block,
            flags=re.DOTALL | re.IGNORECASE
        )

        option_matches = re.findall(
            r"\(([a-e])\)\s*(.*?)(?=\([a-e]\)|Ans\.|$)",
            block,
            flags=re.DOTALL | re.IGNORECASE
        )

        answer_match = re.search(
            r"Ans\.\(([a-e])\)",
            block,
            flags=re.IGNORECASE
        )

        question_text = ""

        if question_match:
            question_text = (
                question_match.group(1)
                .strip()
            )

        options = []

        for _, option_text in option_matches:

            options.append(
                option_text.strip()
            )

        correct_answer = None

        if answer_match:
            correct_answer = (
                answer_match.group(1)
                .lower()
            )

        questions.append(
            {
                "section": "General",
                "question": question_text,
                "options": options,
                "correct_answer":
                correct_answer
            }
        )

    return questions