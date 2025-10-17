from typing import Annotated
from fastapi import Depends, Query, Body, Request
from pydantic import BaseModel

from src.schemas.rooms import RoomPATCHRequest
from src.exceptions import NoAccessTokenHTTPException
from src.services.auth import AuthService
from src.database import async_session
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="Page number", ge=1)]
    per_page: Annotated[
        int | None, Query(10, description="Number of hotels on the page", ge=1, le=30)
    ]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if not token:
        raise NoAccessTokenHTTPException
    return token


def get_current_user_id(token: str = Depends(get_token)):
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]

