from fastapi import APIRouter, Depends, responses
from prometheus_client import Counter
from sqlalchemy.orm import Session

from controller import auth as authorized
from controller.account import AccountOperations
from controller.users import UserOperations
from plugins import producer
from schemas import error, users
from utils import password, session

router = APIRouter()

msg_sender = producer.Producer()

admin_counter = Counter("new_admin_users", "Number of admin users")


@router.post(
    "/register",
    response_model=users.User,
    responses={
        401: {"model": error.UserNotFound},
    },
)
async def register_user(
    login: users.RegisterUser,
    db: Session = Depends(session.create),
):
    """
    This API is used to register
    a new user into the system

    It takes the following:
     - username: str
     - email: str
     - password: str
    """
    user_operation = UserOperations(db)
    account_operation = AccountOperations(db)
    user = user_operation.register_user(login)
    account_operation.create_account(user.id)
    auth = authorized.Auth()
    token = auth.create_access_token(subject=user.id)
    msg_sender.send_message(
        "new_users",
        {
            "username": login.username,  # type: ignore
            "email": login.email,
            "token": token,
        },
    )
    return user


@router.post(
    "/change/email",
    response_model=users.ChangeOut,
    responses={
        401: {"model": error.UserNotFound},
        404: {"model": error.UnAuthorizedError},
    },
)
async def change_email(
    data: users.ChangeEmail,
    _: str = Depends(authorized.bearerschema),
    authorize: authorized.Auth = Depends(),
    db: Session = Depends(session.create),
):
    """
    This API is used to change
    the email of an
    authenticated user
    It takes the following:
     - email: str
    """
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user_operation = UserOperations(db)
    user_operation.reset_user_email(user_id, data.email)
    return responses.JSONResponse(
        content={"message": "email changed successfully"}, status_code=200
    )


@router.post(
    "/change/username",
    response_model=users.ChangeOut,
    responses={
        401: {"model": error.UserNotFound},
        404: {"model": error.UnAuthorizedError},
    },
)
async def change_username(
    data: users.ChangeUsername,
    _: str = Depends(authorized.bearerschema),
    authorize: authorized.Auth = Depends(),
    db: Session = Depends(session.create),
):
    """
    This API is used to change the
    username of an authenticated user
    It takes the following data:
      - username: str

    """
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user_operation = UserOperations(db)
    user_operation.reset_user_username(user_id, data.username)
    return responses.JSONResponse(
        content={"message": "username changed successfully"}, status_code=200
    )


@router.post(
    "/change/password",
    response_model=users.ChangeOut,
    responses={
        401: {"model": error.UserNotFound},
        404: {"model": error.UnAuthorizedError},
    },
)
async def change_password(
    _: str = Depends(authorized.bearerschema),
    authorize: authorized.Auth = Depends(),
):
    """
    This API is used to generate a token
    to change the password of an
    authenticated user
    """
    authorize.jwt_required()
    access_token = authorize.create_access_token(
        subject=authorize.get_jwt_subject(), fresh=True  # type: ignore
    )
    return responses.JSONResponse(
        content={"access_token": access_token}, status_code=200
    )


@router.post(
    "/change/password/confirm",
    response_model=users.ChangeOut,
    responses={
        401: {"model": error.UserNotFound},
        404: {"model": error.UnAuthorizedError},
    },
)
async def confirm_password_change(
    data: users.ChangePassword,
    _: str = Depends(authorized.bearerschema),
    authorize: authorized.Auth = Depends(),
    db: Session = Depends(session.create),
):
    """
    This API is used to change
    the password of an
    authenticated user
    The payload takes:
      - password: str
    """
    authorize.fresh_jwt_required()
    user_id = authorize.get_jwt_subject()
    user_operation = UserOperations(db)
    user_operation.reset_user_password(user_id, data.password)
    return responses.JSONResponse(
        content={"message": "changed password successfully"}, status_code=200
    )


@router.get(
    "/username",
    response_model=users.ChangeOut,
    responses={
        401: {"model": error.UserNotFound},
        404: {"model": error.UnAuthorizedError},
    },
)
async def get_username(
    _: str = Depends(authorized.bearerschema),
    authorize: authorized.Auth = Depends(),
    db: Session = Depends(session.create),
):
    """
    This API is used to get
    a username of an
    authenticated user
    """
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user_operation = UserOperations(db)
    username = user_operation.get_username(user_id)
    return responses.JSONResponse(
        content={"message": username}, status_code=200  # type: ignore
    )


@router.post(
    "/admin",
    response_model=users.AdminOut,
    responses={
        401: {"model": error.UserNotFound},
        404: {"model": error.UnAuthorizedError},
    },
)
async def add_an_administrator(
    data: users.AdminUser,
    _: str = Depends(authorized.bearerschema),
    authorize: authorized.Auth = Depends(),
    db: Session = Depends(session.create),
):
    """
    This API is used to
    add of an administrator user
    """
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user_operation = UserOperations(db)
    user_operation.check_if_email_is_verified(user_id)
    user_operation.set_user_as_admin(user_id, data.username)
    user_details = user_operation.get_user_by(data.username)
    admin_password = password.generate_password()
    msg_sender.send_message(
        "add_admin",
        {
            "username": data.username,  # type: ignore
            "email": user_details.email,
            "password": admin_password,
        },
    )
    admin_counter.inc()
    return responses.JSONResponse(
        content={
            "message": f"{data.username} is now an admin",
            "password": admin_password,
        },  # type: ignore
        status_code=200,
    )
