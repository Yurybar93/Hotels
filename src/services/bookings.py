from src.exceptions import AllRoomsBookedException, AllRoomsBookedHTTPException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.services.base import BaseService
from src.services.rooms import RoomService


class BookingService(BaseService):
    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(self, booking_data: BookingAddRequest, user_id: int):
        room = await RoomService(self.db).check_room_with_exceptions(
            self.db.rooms.get_one(id=booking_data.room_id)
        )

        _booking_data = BookingAdd(**booking_data.model_dump(), user_id=user_id, price=room.price)
        try:
            booking = await self.db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
        except AllRoomsBookedException:
            raise AllRoomsBookedHTTPException
        await self.db.commit()
        return booking
