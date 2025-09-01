from sqlalchemy import select
from repositories.base import BaseRepository
from repositories.mappers.mappers import BookingDataMapper
from src.schemas.bookings import Booking
from src.models.bookings import BookingsOrm

class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper