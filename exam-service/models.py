from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text
)

from database import Base


class Exam(Base):

    __tablename__ = "exams"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String
    )

    total_questions = Column(
        Integer
    )


class Section(Base):

    __tablename__ = "sections"

    id = Column(
        Integer,
        primary_key=True
    )

    exam_id = Column(
        Integer,
        ForeignKey(
            "exams.id"
        )
    )

    name = Column(
        String
    )

    total_questions = Column(
        Integer
    )

    timer_minutes = Column(
        Integer
    )

    
class Question(Base):

    __tablename__ = "questions"

    id = Column(
        Integer,
        primary_key=True
    )

    section_id = Column(
        Integer,
        ForeignKey(
            "sections.id"
        )
    )

    question_text = Column(
        Text
    )

    option_a = Column(String)

    option_b = Column(String)

    option_c = Column(String)

    option_d = Column(String)

    option_e = Column(String)

    correct_answer = Column(
        String,
        nullable=True
    )

    image_path = Column(
        String,
        nullable=True
    )