import fastapi
from fastapi import responses
from prometheus_client import Gauge
from sqlalchemy.orm import Session

from controller import account as acc
from controller import auth as authorized
from controller import users
from schemas import account, error
from utils import session

router = fastapi.APIRouter()
gauge = Gauge(
    name="number_of_active_users_total",  # type: ignore
    documentation="Number of active users",
)


@router.post(
    "/login",
    response_model=account.LoginOut,
    responses={404: {"model": error.UnAuthorizedError}},
)
async def login(
    login: account.Login, db: Session = fastapi.Depends(session.create)  # noqa: E501
):
    """
    This API Route is used to log a User
    into the System

    The payload consist of the following:
     - username: 'username'
     - password: 'password'


    """
    user_operation = users.UserOperations(db)
    user_id = user_operation.verify_user(login)
    acc.AccountOperations(db).set_account_as_active(user_id)
    auth = authorized.Auth()
    access_token = auth.create_access_token(subject=user_id)
    refresh_token = auth.create_refresh_token(subject=user_id)
    gauge.inc()
    payload = {"access_token": access_token, "refresh_token": refresh_token}
    return responses.JSONResponse(content=payload, status_code=200)


@router.post(
    "/logout",
)
async def logout(
    _: str = fastapi.Depends(authorized.bearerschema),
    authorize: authorized.Auth = fastapi.Depends(),
    db: Session = fastapi.Depends(session.create),
):
    """
    This API route is used to logout a
    User Account
    """
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    token_id = authorize.get_raw_jwt().get("jti")
    user_operation = users.UserOperations(db)
    user_operation.check_if_email_is_verified(user_id)
    authorized.redis_connection.set_value(token_id, "true")
    acc.AccountOperations(db).set_account_as_inactive(user_id)
    gauge.dec()
    return responses.JSONResponse(
        content={"message": "logout successfully"}, status_code=200
    )


@router.post(
    "/refresh",
    responses={
        404: {"model": error.InvalidRefreshToken},
    },
)
async def get_new_access_token(
    _: str = fastapi.Depends(authorized.bearerschema),
    authorize: authorized.Auth = fastapi.Depends(),
):
    """
    This API route is use to generate a
    new Access token
    """
    authorize.jwt_refresh_token_required()
    user_id = authorize.get_jwt_subject()
    access_token = authorize.create_access_token(user_id)
    return responses.JSONResponse(
        content={"access_token": access_token}, status_code=200
    )


@router.get(
    "/verify/account",
    responses={404: {"model": error.UnAuthorizedError}},
)
async def verify_user_account(
    token: str,
    db: Session = fastapi.Depends(session.create),
    authorize: authorized.Auth = fastapi.Depends(),  # noqa: E501
):
    """
    This API Route is used to verify a user account
    through email verification

    Takes a token parameter
    """
    user_id = authorize.get_raw_jwt(token)["sub"]
    user_operation = users.UserOperations(db)
    user_operation.set_email_as_verified(user_id)
    return responses.FileResponse(
        "static/index.html",
        media_type="text/html",
        status_code=200,
    )
