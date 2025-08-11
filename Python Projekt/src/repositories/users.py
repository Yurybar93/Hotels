from models.users import UsersOrm
from repositories.base import BaseRepository
from schemas.users import User


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User