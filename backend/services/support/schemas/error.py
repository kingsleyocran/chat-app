import pydantic


class InvalidStringError(pydantic.BaseModel):
    detail: str = "String too long"


class MLModelNotFoundError(pydantic.BaseModel):
    detail: str = "ML model not found"
