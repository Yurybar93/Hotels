from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from src.exceptions import ObjectNotFoundException
from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPasswort


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_passwort(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        try:
            result = await self.session.execute(query)
            model = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return UserWithHashedPasswort.model_validate(model, from_attributes=True)
