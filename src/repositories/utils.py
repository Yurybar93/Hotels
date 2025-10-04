from datetime import date
from sqlalchemy import select, func
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.database import engine


def room_ids_for_booking(date_from: date, date_to: date, hotel_id: int | None = None):
    rooms_count = (
        select(BookingsOrm.room_id, func.count("*").label("room_booked"))
        .select_from(BookingsOrm)
        .filter(BookingsOrm.date_from <= date_to, BookingsOrm.date_to >= date_from)
        .group_by(BookingsOrm.room_id)
        .cte("rooms_count")
    )

    free_rooms_table = (
        select(
            RoomsOrm.id.label("room_id"),
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.room_booked, 0)).label("free_rooms"),
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
        .cte("free_rooms_table")
    )

    room_ids_for_hotel = select(RoomsOrm.id).select_from(RoomsOrm)
    if hotel_id is not None:
        room_ids_for_hotel = room_ids_for_hotel.filter_by(hotel_id=hotel_id)

    room_ids_for_hotel = room_ids_for_hotel.subquery(name="room_ids_for_hotel")

    room_ids_get = (
        select(free_rooms_table.c.room_id)
        .select_from(free_rooms_table)
        .filter(
            free_rooms_table.c.free_rooms > 0,
            free_rooms_table.c.room_id.in_(room_ids_for_hotel),
        )
    )

    print(room_ids_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))
    return room_ids_get
