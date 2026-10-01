from unittest import result
from pdf_service import (
    generate_result_pdf
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from exam_service import ExamService
from services.email_service import (
    send_result_email
)
from fastapi.responses import FileResponse
from database import (
    engine,
    SessionLocal
)
from html_pdf_service import (
    generate_html_pdf
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

    print("\n========== SAVE DEBUG ==========")
    print("TOTAL QUESTIONS:", len(questions))

    if questions:
        print("FIRST QUESTION:")
        print(questions[0])

        print(
            "FIRST QUESTION SECTION:",
            questions[0].get("section")
        )

    print("================================\n")

    return service.create_exam(
        questions
    )

@app.get("/test-html-pdf")
def test_html_pdf():

    pdf_path = (
        "results/result_page.pdf"
    )

    generate_html_pdf(
        "https://pdf2exam.org/result",
        pdf_path,
    )

    return {
        "pdf_path": pdf_path
    }
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

    correct = data.get("correct", 0)
    incorrect = data.get("incorrect", 0)
    unseen = data.get("unseen", 0)

    accuracy = data.get(
        "accuracy",
        "0.00"
    )

    completion_percentage = data.get(
        "completion_percentage",
        "0.00"
    )

    correct_percentage = data.get(
        "correct_percentage",
        "0.00"
    )

    total_time = data.get(
        "total_time",
        0
    )

    utilized_time = data.get(
        "utilized_time",
        0
    )

    section_stats = data.get(
        "section_stats",
        {}
    )

    questions = data.get(
        "questions",
        []
    )

    answers = data.get(
        "answers",
        {}
    )

    pdf_path = generate_result_pdf(
        user_name=user_name,
        email=email,

        score=score,
        total_questions=total_questions,

        attempted=attempted,
        correct=correct,
        incorrect=incorrect,

        skipped=skipped,
        review=review,
        unseen=unseen,

        accuracy=accuracy,

        completion_percentage=completion_percentage,

        correct_percentage=correct_percentage,

        total_time=total_time,

        utilized_time=utilized_time,

        section_stats=section_stats,

        questions=questions,

        answers=answers,
    )

    email_sent = send_result_email(
        email,
        "PDF2Exam",
        score,
        total_questions,
        pdf_path,
    )

    return {
        "message": "PDF generated",
        "pdf_path": pdf_path,
        "email_sent": email_sent,
    }

@app.get("/result-page-pdf")
def result_page_pdf():

    pdf_path = "results/result_page.pdf"

    generate_html_pdf(
        "https://pdf2exam.org/result",
        pdf_path,
    )

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="result_page.pdf"
    )
