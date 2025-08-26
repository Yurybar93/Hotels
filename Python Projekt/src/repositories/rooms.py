from sqlalchemy import select, func
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room
from src.models.rooms import RoomsOrm
from src.database import engine



class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            date_from,
            date_to,
            hotel_id
    ):
        '''
        with rooms_count as (
SELECT room_id, count(*) as room_booked FROM bookings
WHERE date_from <= '2025-08-30' and date_to >= '2025-07-01'
GROUP BY room_id
),
free_rooms_table as (
select rooms.id, quantity - coalesce(room_booked, 0) as free_rooms    from rooms
left join rooms_count
on rooms.id = rooms_count.room_id
)
select * from free_rooms_table
where free_rooms > 0
        '''

        rooms_count = (
            select(BookingsOrm.id,func.count('*').label('room_booked'))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= date_to,
                BookingsOrm.date_to >= date_from
            )
            .group_by(BookingsOrm.room_id)
            .cte('rooms_count')
        )

        free_rooms_table = (
            select(
                RoomsOrm.id,
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.room_booked, 0)).label('free_rooms')
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.id)
            .cte('free_rooms_table')
        )

        query = (
            select(free_rooms_table)
            .select_from(free_rooms_table)
            .filter(free_rooms_table.c.free_rooms > 0)
        )

        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))