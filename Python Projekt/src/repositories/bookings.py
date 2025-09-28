from datetime import date
from sqlalchemy import select

from src.exceptions import AllRoomsBookedException
from src.repositories.utils import room_ids_for_booking
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.models.bookings import BookingsOrm


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_booking_with_checkin_today(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, data, hotel_id):
        room_ids_get = room_ids_for_booking(data.date_from, data.date_to, hotel_id)
        room_ids_get_res = await self.session.execute(room_ids_get)
        room_ids_to_book: list[int] = room_ids_get_res.scalars().all()

        if data.room_id in room_ids_to_book:
            booking = await self.add(data)
            return booking
        raise AllRoomsBookedException
