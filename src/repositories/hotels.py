from sqlalchemy import func, select

from src.repositories.mappers.mappers import HotelDataMapper
from src.models.rooms import RoomsOrm
from src.repositories.utils import room_ids_for_booking
from src.schemas.hotels import Hotel
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel
    mapper = HotelDataMapper

    async def get_all(self, title, location, limit, offset) -> list[Hotel]:
        query = select(HotelsOrm)
        if title:
            query = query.where(HotelsOrm.title.ilike(f"%{title}%"))
        if location:
            query = query.where(HotelsOrm.location.ilike(f"%{location}%"))
        query = query.limit(limit).offset(offset)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [
            Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()
        ]

    async def get_filtered_by_time(self, date_from, date_to, title, location, limit, offset):
        rooms_ids_get = room_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_get = (
            select(RoomsOrm.hotel_id).select_from(RoomsOrm).filter(RoomsOrm.id.in_(rooms_ids_get))
        )

        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_get))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        hotels = result.scalars().all()
        print(query.compile(compile_kwargs={"literal_binds": True}))
        return [self.mapper.map_to_domain_entity(hotel) for hotel in hotels]
