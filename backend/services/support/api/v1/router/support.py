import fastapi

from core import model
from error import exceptions
from schemas import error, support

router = fastapi.APIRouter()

dave_model = model.DaveModel()


@router.post(
    "/support",
    response_model=support.AnswerOut,
    responses={
        400: {"model": error.InvalidStringError},
        500: {"model": error.MLModelNotFoundError},
    },
)
async def support_question_and_answer(
    text: support.AnswerIn = fastapi.Body(default=None),
) -> dict[str, str]:
    """
    This API is used for conservation
    """

    if dave_model.get_model() is None:
        raise exceptions.ModelError(msg="Model not loaded", status_code=500)

    reply = dave_model.reply(question=text.question)
    response: dict[str, str] = {"answer": reply}
    return response
