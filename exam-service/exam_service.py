import json

from database import SessionLocal

from models import (
    Exam,
    Section,
    Question
)


class ExamService:

    def create_exam(
        self,
        questions
    ):

        db = SessionLocal()

        exam = Exam(
            name="Generated Exam",
            total_questions=len(questions)
        )

        db.add(exam)
        db.commit()
        db.refresh(exam)

        sections_map = {}

        for q in questions:

            section_name = q.get(
                "section",
                "General"
            )

            if section_name not in sections_map:

                section_question_count = len(
                    [
                        question
                        for question in questions
                        if question.get(
                            "section",
                            "General"
                        ) == section_name
                    ]
                )

                section = Section(
                    exam_id=exam.id,
                    name=section_name,
                    total_questions=section_question_count,
                    timer_minutes=60
                )

                db.add(section)
                db.commit()
                db.refresh(section)

                sections_map[
                    section_name
                ] = section

        for q in questions:

            options = q.get(
                "options",
                []
            )

            section_name = q.get(
                "section",
                "General"
            )

            section = sections_map[
                section_name
            ]

            print(
                "SAVING:",
                q.get(
                    "question",
                    ""
                )[:50],
                "SECTION:",
                section_name,
                "IS_CODE:",
                q.get(
                    "is_code"
                )
            )

            question = Question(
                section_id=section.id,

                question_text=q.get(
                    "question",
                    ""
                ),

                directions=q.get(
                    "description"
                ),

                is_code=q.get(
                    "is_code",
                    False
                ),

                shared_image_path=q.get(
                    "image_path"
                ),

                image_path=q.get(
                    "image_path"
                ),

                table_data=(
                    json.dumps(
                        q.get(
                            "table_data"
                        )
                    )
                    if q.get(
                        "table_data"
                    ) is not None
                    else None
                ),

                option_a=(
                    options[0]
                    if len(options) > 0
                    else ""
                ),

                option_b=(
                    options[1]
                    if len(options) > 1
                    else ""
                ),

                option_c=(
                    options[2]
                    if len(options) > 2
                    else ""
                ),

                option_d=(
                    options[3]
                    if len(options) > 3
                    else ""
                ),

                option_e=(
                    options[4]
                    if len(options) > 4
                    else ""
                ),

                correct_answer=q.get(
                    "correct_answer"
                )
            )

            db.add(question)

        db.commit()

        exam_id = exam.id

        db.close()

        return {
            "status": "saved",
            "exam_id": exam_id,
            "questions": len(questions)
        }