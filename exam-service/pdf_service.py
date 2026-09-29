import os
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
)


def generate_result_pdf(
    user_name: str,
    email: str,
    exam_name: str,
    score: int,
    total_questions: int,
    attempted: int,
    skipped: int,
    review: int,
):

    os.makedirs(
        "results",
        exist_ok=True
    )

    file_name = (
        f"results/result_"
        f"{datetime.now().timestamp()}.pdf"
    )

    doc = SimpleDocTemplate(
        file_name
    )

    styles = (
        getSampleStyleSheet()
    )

    content = [

        Paragraph(
            "PDF2Exam Result Report",
            styles["Title"]
        ),

        Spacer(1, 20),

        Paragraph(
            f"Candidate Name: {user_name}",
            styles["Normal"]
        ),

        Paragraph(
            f"Email: {email}",
            styles["Normal"]
        ),

        Paragraph(
            f"Exam: {exam_name}",
            styles["Normal"]
        ),

        Spacer(1, 10),

        Paragraph(
            f"Score: {score}/{total_questions}",
            styles["Normal"]
        ),

        Paragraph(
            f"Attempted: {attempted}",
            styles["Normal"]
        ),

        Paragraph(
            f"Skipped: {skipped}",
            styles["Normal"]
        ),

        Paragraph(
            f"Review: {review}",
            styles["Normal"]
        ),

    ]

    doc.build(content)

    return file_name