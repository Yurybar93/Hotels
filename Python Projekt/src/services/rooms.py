from datetime import date
from sqlalchemy.exc import DBAPIError
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPATCH, RoomPATCHRequest
from src.exceptions import (
    ForeinKeyRoomViolationException,
    ForeinKeyViolationException,
    HotelNotFoundException,
    ObjectNotFoundException,
    RoomNotFoundException,
    UncorrectDataException,
    UncorrectHotelDataException,
    UncorrectRoomDataException,
    check_date_from_bigger_than_date_to,
)
from src.services.base import BaseService


class RoomService(BaseService):
    async def get_rooms(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        check_date_from_bigger_than_date_to(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room(self, hotel_id: int, room_id: int):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        except UncorrectDataException:
            raise UncorrectHotelDataException
        return await self.db.rooms.get_filtered_with_facilities(id=room_id, hotel_id=hotel_id)

    async def create_room(self, hotel_id: int, room_data: RoomAddRequest):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        except UncorrectDataException:
            raise UncorrectHotelDataException
        _room_data = RoomAdd(**room_data.model_dump(), hotel_id=hotel_id)
        room = await self.db.rooms.add(_room_data)

        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=facility_id)
            for facility_id in room_data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()

    async def update_room(self, hotel_id: int, room_id: int, room_data: RoomAddRequest):
        _room_data = RoomAdd(**room_data.model_dump(), hotel_id=hotel_id)
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        except UncorrectDataException:
            raise UncorrectHotelDataException
        try:
            await self.db.rooms.edit(_room_data, id=room_id)
            await self.db.rooms_facilities.set_room_facilities(
                room_id, facility_ids=room_data.facilities_ids
            )
        except ObjectNotFoundException:
            raise RoomNotFoundException
        except UncorrectDataException:
            raise UncorrectRoomDataException
        await self.db.commit()

    async def patch_room(self, hotel_id: int, room_id: int, room_data: RoomPATCHRequest):
        room_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPATCH(**room_dict, hotel_id=hotel_id)
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        except UncorrectDataException:
            raise UncorrectHotelDataException
        try:
            await self.db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        except UncorrectDataException:
            raise UncorrectRoomDataException
        if "facilities_ids" in room_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id, facility_ids=room_dict["facilities_ids"]
            )
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        except UncorrectDataException:
            raise UncorrectHotelDataException
        try:
            await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        except ForeinKeyViolationException:
            raise ForeinKeyRoomViolationException
        except UncorrectDataException:
            raise UncorrectRoomDataException
        await self.db.commit()
