from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from exam_service import ExamService

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
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = ExamService()


@app.on_event("startup")
def startup():

    Base.metadata.drop_all( bind=engine)

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "Database recreated."
    )


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
        db.query(Question)
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
            "question": q.question_text,
            "description": q.directions,
            "shared_image_path": q.shared_image_path,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
            "option_e": q.option_e,
            "correct_answer": q.correct_answer,
            "image_path": q.image_path
        }
        for q in questions
    ]

    db.close()

    return {
        "questions": result
    }