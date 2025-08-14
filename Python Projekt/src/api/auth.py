from fastapi import APIRouter, Body, HTTPException, Response

from api.dependecies import UserIdDep
from repositories.users import UsersRepository
from services.auth import AuthService
from src.database import async_session
from schemas.users import UserAdd, UserLogin, UserRequestAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/login")
async def login_user(
    data: UserLogin,
    response: Response,
):
    async with async_session() as session:
        user = await UsersRepository(session).get_user_with_hashed_passwort(email=data.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}

@router.post("/register")
async def register_user(
    data: UserRequestAdd = Body(openapi_examples={
        "1": {
            "summary": "User",
            "description": "Create a new user with the provided data.",
            "value": {
                "first_name": "Muster",
                "last_name": "Mustermann",
                "email": "mustermann@muster.com",
                "password": "12345678"
            }
        }
    })
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        hashed_password=hashed_password
        )
    async with async_session() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status": "OK"}


@router.get("/me")
async def get_me(user_id: UserIdDep):
    async with async_session() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
    return user

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}