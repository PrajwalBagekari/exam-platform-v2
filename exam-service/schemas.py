from pydantic import BaseModel


class ExamCreate(
    BaseModel
):

    questions: list