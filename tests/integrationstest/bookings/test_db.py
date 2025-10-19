from datetime import date
from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2023, month=10, day=10),
        date_to=date(year=2023, month=10, day=15),
        price=5000,
    )

    new_booking = await db.bookings.add(booking_data)

    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert new_booking.id == booking.id
    assert new_booking.user_id == booking.user_id
    assert new_booking.room_id == booking.room_id

    update_price = 6000
    update_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2023, month=10, day=16),
        date_to=date(year=2023, month=10, day=20),
        price=update_price,
    )

    await db.bookings.edit(update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.price == update_price

    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking is None
