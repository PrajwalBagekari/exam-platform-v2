import os
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
)


def get_option_text(
    question,
    answer,
):
    mapping = {
        "A": question.get("option_a"),
        "B": question.get("option_b"),
        "C": question.get("option_c"),
        "D": question.get("option_d"),
        "E": question.get("option_e"),
    }

    return mapping.get(
        str(answer).upper(),
        "Not Answered"
    )


def generate_result_pdf(
    user_name,
    email,

    score,
    total_questions,

    attempted,
    correct,
    incorrect,

    skipped,
    review,
    unseen,

    accuracy,

    completion_percentage,

    correct_percentage,

    total_time,
    utilized_time,

    section_stats,

    questions,

    answers,
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

    styles = getSampleStyleSheet()

    content = []

    # =========================
    # HEADER
    # =========================

    content.append(
        Paragraph(
            "PDF2Exam Result Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # =========================
    # CANDIDATE DETAILS
    # =========================

    content.append(
        Paragraph(
            "<b>Candidate Details</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Name: {user_name}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Email: {email}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 15)
    )

    # =========================
    # OVERALL PERFORMANCE
    # =========================

    content.append(
        Paragraph(
            "<b>Overall Performance</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Score: {score}/{total_questions}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Attempted: {attempted}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Correct: {correct}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Incorrect: {incorrect}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Skipped: {skipped}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Review: {review}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Unseen: {unseen}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Accuracy: {accuracy}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Completion Percentage: {completion_percentage}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Correct Percentage: {correct_percentage}%",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 15)
    )

    # =========================
    # TIME ANALYSIS
    # =========================

    content.append(
        Paragraph(
            "<b>Time Analysis</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Total Time: {total_time} Min",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Utilized Time: {utilized_time} Min",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # =========================
    # SECTION ANALYSIS
    # =========================

    content.append(PageBreak())

    content.append(
        Paragraph(
            "Sectional Analysis",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 15)
    )

    for section_name, stats in section_stats.items():

        content.append(
            Paragraph(
                section_name,
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                f"Total Questions: {stats.get('total', 0)}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Attempted: {stats.get('attempted', 0)}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Correct: {stats.get('correct', 0)}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Incorrect: {stats.get('incorrect', 0)}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Skipped: {stats.get('skipped', 0)}",
                styles["Normal"]
            )
        )

        content.append(
            Spacer(1, 12)
        )

    # =========================
    # QUESTION REVIEW
    # =========================

    content.append(PageBreak())

    content.append(
        Paragraph(
            "Question Review",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 15)
    )

    for index, question in enumerate(
        questions
    ):

        question_number = (
            index + 1
        )

        selected_answer = (
            answers.get(
                str(question_number)
            )
            or answers.get(
                question_number
            )
        )

        correct_answer = question.get(
            "correct_answer"
        )

        is_correct = (
            selected_answer
            and
            str(selected_answer).lower()
            ==
            str(correct_answer).lower()
        )

        content.append(
            Paragraph(
                f"<b>Question {question_number}</b>",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                question.get(
                    "question",
                    ""
                ),
                styles["Normal"]
            )
        )

        content.append(
            Spacer(1, 5)
        )

        if selected_answer:

            content.append(
                Paragraph(
                    f"Your Answer: "
                    f"{selected_answer}. "
                    f"{get_option_text(question, selected_answer)}",
                    styles["Normal"]
                )
            )

        else:

            content.append(
                Paragraph(
                    "Your Answer: Not Answered",
                    styles["Normal"]
                )
            )

        content.append(
            Paragraph(
                f"Correct Answer: "
                f"{correct_answer}. "
                f"{get_option_text(question, correct_answer)}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                (
                    "✅ Correct"
                    if is_correct
                    else
                    "❌ Incorrect"
                ),
                styles["Normal"]
            )
        )

        content.append(
            Spacer(1, 12)
        )

    doc.build(content)

    return file_name