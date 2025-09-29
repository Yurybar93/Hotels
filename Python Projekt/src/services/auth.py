from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
import jwt

from src.exceptions import (
    InvalidTokenHTTPException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    UncorrectPasswordException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.schemas.users import UserAdd, UserLogin, UserRequestAdd
from src.config import settings
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise InvalidTokenHTTPException

    async def register_user(self, data: UserRequestAdd):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            hashed_password=hashed_password,
        )
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise UserAlreadyExistsException

    async def login_user(self, data: UserLogin):
        try:
            user = await self.db.users.get_user_with_hashed_passwort(email=data.email)
        except ObjectNotFoundException:
            raise UserNotFoundException
        if not self.verify_password(data.password, user.hashed_password):
            raise UncorrectPasswordException
        access_token = self.create_access_token({"user_id": user.id})
        return access_token

    async def get_user(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)
