from datetime import date
from src.schemas.bookings import BookingAdd


async def test_add_hotel(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id = user_id,
        room_id = room_id,
        date_from = date(year=2023, month=10, day=10),
        date_to = date(year=2023, month=10, day=15),
        price = 5000,
        )
    
    await db.bookings.add(booking_data)

    new_booking_data = BookingAdd(
        user_id = user_id,
        room_id = room_id,
        date_from = date(year=2023, month=10, day=16),
        date_to = date(year=2023, month=10, day=20),
        price = 6000,
        )
    booking_id = (await db.bookings.get_all())[0].id

    await db.bookings.edit(new_booking_data, id=booking_id)
    await db.bookings.delete(id=booking_id)
    await db.commit()