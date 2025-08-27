from datetime import date
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room
from src.models.rooms import RoomsOrm

from src.repositories.utils import room_ids_for_booking



class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            hotel_id: int
    ):  
        room_ids_get = room_ids_for_booking(date_from, date_to, hotel_id)
        #print(room_ids_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        return await self.get_filtered(RoomsOrm.id.in_(room_ids_get))