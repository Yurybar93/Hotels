from fastapi import APIRouter, Body

from passlib.context import CryptContext

from repositories.users import UsersRepository
from schemas.hotels import HotelAdd
from src.database import async_session
from schemas.users import UserAdd, UserRequestAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    hashed_password = pwd_context.hash(data.password)
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