from unittest import result

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.email_service import (
    send_result_email
)
from database import (
    engine,
    SessionLocal
)

from models import (
    Base,
    Exam,
    Question,
    Section
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pdf2exam.org"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = ExamService()


@app.on_event("startup")
def startup():

    Base.metadata.create_all(
        bind=engine
    )

    print("Database ready.")


@app.get("/")
def root():

    return {
        "service": "exam-service",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/save")
def save(data: dict):

    questions = data.get(
        "questions",
        []
    )

    return service.create_exam(
        questions
    )


@app.get("/exam/{exam_id}")
def get_exam(
    exam_id: int
):

    db = SessionLocal()

    exam = db.query(
        Exam
    ).filter(
        Exam.id == exam_id
    ).first()

    db.close()

    if not exam:

        return {
            "message": "not found"
        }

    return {
        "id": exam.id,
        "name": exam.name,
        "total_questions": exam.total_questions
    }


@app.get("/exam/{exam_id}/questions")
def get_exam_questions(
    exam_id: int
):

    db = SessionLocal()

    questions = (
        db.query(
            Question,
            Section
        )
        .join(
            Section,
            Question.section_id == Section.id
        )
        .filter(
            Section.exam_id == exam_id
        )
        .all()
    )

    result = [
        {
            "id": q.id,
            "section": section.name,
            "question": q.question_text,
            "description": q.directions,
            "is_code": q.is_code,
            "shared_image_path": q.shared_image_path,
            "table_data": q.table_data,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
            "option_e": q.option_e,
            "correct_answer": q.correct_answer,
            "image_path": q.image_path
        }
        for q, section in questions
    ]
    print("FIRST QUESTION:")
    print(result[0] if result else "NO QUESTIONS")


    db.close()

    return {
        "questions": result
    }
@app.post("/submit-result")
def submit_result(data: dict):

    user_name = data["user_name"]
    email = data["email"]

    score = data["score"]
    total_questions = data["total_questions"]

    attempted = data["attempted"]
    skipped = data["skipped"]
    review = data["review"]

    # generate_result_pdf(...)
    # send_result_email(...)

    return {
        "message": "Result email sent"
    }
