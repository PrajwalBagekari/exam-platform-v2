import json
from database import (
    SessionLocal
)

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
                total_questions=len(
                    questions
                )
            )

            db.add(exam)

            db.commit()

            db.refresh(exam)

            # section = Section(
            #     exam_id=exam.id,
            #     name="General",
            #     total_questions=len(
            #         questions
            #     ),
            #     timer_minutes=60
            # )

            # db.add(section)

            # db.commit()

            # db.refresh(section)
            sections = {}

            for q in questions:
                section_name = q.get(
                    "section",
                    "General"
                )

                if section_name not in sections:

                    section = Section(
                        exam_id=exam.id,
                        name=section_name,
                        total_questions=0,
                        timer_minutes=0
                    )

                    db.add(section)

                    db.flush()

                    sections[section_name] = section

                sections[
                    section_name
                ].total_questions += 1
                print(
                    "SECTION RECEIVED:",
                    q.get("section")
                )

                print(
                    "QUESTION:",
                    q.get("question", "")[:50]
                )

                options = q.get(
                    "options",
                    []
                )
                print(
                    "SAVING:",
                    q.get("question", "")[:50],
                    "IS_CODE:",
                    q.get("is_code")
                )

                question = Question(
                    section_id=sections[
                        section_name
                    ].id,

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
                        "image_path",
                    ),

                    image_path=q.get(
                        "image_path",
                    ),
                    
                    table_data=(
                        json.loads(
                            q.get("table_data")
                        )
                        if q.get("table_data")
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
            for section in sections.values():

                if (
                    section.total_questions > 0
                ):

                    if not section.timer_minutes:

                        section.timer_minutes = (
                            section.total_questions
                        )

            db.commit()

            exam_id = exam.id

            db.close()

            return {
                "status": "saved",
                "exam_id": exam_id,
                "questions": len(questions)
            }
