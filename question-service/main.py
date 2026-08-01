from fastapi import FastAPI

from question_parser import (
    extract_questions
)

app = FastAPI()


@app.get("/")
def root():

    return {
        "service": "question-service",
        "status": "running"
    }


@app.post("/questions")
def questions(data: dict):

    print("=" * 60)
    print("QUESTION SERVICE")

    print("REQUEST DATA:")
    print(data)

    text = data.get(
        "text",
        ""
    )

    print("=" * 60)
    print("TEXT RECEIVED:")
    print(text[:2000])

    extracted_questions = extract_questions(
        text
    )

    print("=" * 60)
    print("QUESTIONS FOUND:")
    print(len(extracted_questions))

    for index, question in enumerate(
        extracted_questions,
        start=1
    ):
        print(
            f"Q{index}:",
            question.get(
                "question",
                ""
            )[:100]
        )

    return {
        "questions":
        extracted_questions
    }