from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.exc import NoResultFound, DBAPIError
from src.exceptions import RoomNotFoundException, UncorrectDataException, UncorrectRoomDataException
from src.repositories.mappers.mappers import RoomDataMapper

from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomWithRls
from src.models.rooms import RoomsOrm

from src.repositories.utils import room_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(self, date_from: date, date_to: date, hotel_id: int):
        room_ids_get = room_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(room_ids_get))
        )
        result = await self.session.execute(query)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        return [
            RoomWithRls.model_validate(model, from_attributes=True)
            for model in result.unique().scalars().all()
        ]

    async def get_filtered_with_facilities(self, **filter_by):
        query = (
            select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by)
        )

        try:
            result = await self.session.execute(query)
            model = result.scalars().one()
        except NoResultFound:
            raise RoomNotFoundException
        except DBAPIError:
            raise UncorrectRoomDataException
        return RoomWithRls.model_validate(model, from_attributes=True)
