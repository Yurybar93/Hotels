from datetime import date
from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.models.bookings import BookingsOrm

class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_booking_with_checkin_today(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]
