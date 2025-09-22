from pydantic import EmailStr
from sqlalchemy import select
from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPasswort


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_passwort(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        if model is None:
            return None
        return UserWithHashedPasswort.model_validate(model, from_attributes=True)