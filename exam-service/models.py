from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey
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
        ForeignKey("exams.id")
    )

    name = Column(String)

    total_questions = Column(Integer)

    timer_minutes = Column(Integer)

class Question(Base):

    __tablename__ = "questions"

    id = Column(
        Integer,
        primary_key=True
    )

    section_id = Column(
        Integer,
        ForeignKey("sections.id")
    )

    question_text = Column(Text)

    directions = Column(
        Text,
        nullable=True
    )

    shared_image_path = Column(
        String,
        nullable=True
    )

    option_a = Column(Text)
    option_b = Column(Text)
    option_c = Column(Text)
    option_d = Column(Text)
    option_e = Column(Text)


    correct_answer = Column(String)

    image_path = Column(String)