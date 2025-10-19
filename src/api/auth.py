from fastapi import APIRouter, Body, Response, Request

from src.exceptions import (
    UncorrectPasswordException,
    UncorrectPasswordHTTPException,
    UserAlreadyExistsException,
    UserAlreadyExistsHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
)
from src.api.dependecies import DBDep, UserIdDep
from services.auth import AuthService
from schemas.users import UserLogin, UserRequestAdd

router = APIRouter(prefix="/auth", tags=["Authorization and Authentication"])


@router.post("/login")
async def login_user(data: UserLogin, response: Response, db: DBDep):
    try:
        access_token = await AuthService(db).login_user(data)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except UncorrectPasswordException:
        raise UncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "User",
                "description": "Create a new user with the provided data.",
                "value": {
                    "first_name": "Muster",
                    "last_name": "Mustermann",
                    "email": "mustermann@muster.com",
                    "password": "12345678",
                },
            }
        }
    ),
):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    return {"status": "OK"}


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    return await AuthService(db).get_user(user_id)


@router.post("/logout")
async def logout_user(request: Request, response: Response):
    if "access_token" not in request.cookies:
        return {"status": "already_logged_out"}

    response.delete_cookie("access_token")
    return {"status": "OK"}
