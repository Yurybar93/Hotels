from src.models.facilities import FacilitiesOrm
from src.schemas.facilities import Facility
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking
from src.models.users import UsersOrm
from src.schemas.users import User
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room
from src.repositories.mappers.base import DataMapper
from src.schemas.hotels import Hotel
from src.models.hotels import HotelsOrm


class HotelDataMapper(DataMapper):
    model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    model = RoomsOrm
    schema = Room


class UserDataMapper(DataMapper):
    model = UsersOrm
    schema = User


class BookingDataMapper(DataMapper):
    model = BookingsOrm
    schema = Booking


class FacilitiesDataMapper(DataMapper):
    model = FacilitiesOrm
    schema = Facility
