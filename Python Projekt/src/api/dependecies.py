from typing import Annotated
from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel

from src.services.auth import AuthService
from src.database import async_session
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="Номер страницы", ge=1)]
    per_page: Annotated[
        int | None, Query(10, description="Количество отелей на странице", ge=1, le=30)
    ]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token


def get_current_user_id(token: str = Depends(get_token)):
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
