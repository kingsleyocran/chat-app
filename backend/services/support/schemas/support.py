import pydantic


class AnswerOut(pydantic.BaseModel):
    answer: str


class AnswerIn(pydantic.BaseModel):
    question: str
