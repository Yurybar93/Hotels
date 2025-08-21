from repositories.base import BaseRepository
from schemas.rooms import Room
from src.models.rooms import RoomsOrm

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room