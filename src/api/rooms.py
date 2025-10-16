from datetime import date
from fastapi import APIRouter, Body, Query

from src.services.rooms import RoomService
from src.exceptions import (
    FacilitisNotExistsHTTPException,
    ForeignKeyViolationErrorHTTPException,
    ForeinKeyRoomViolationException,
    ForeinKeyViolationException,
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    ObjectAlreadyExistsException,
    RoomAlreadyExistsHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    UncorrectFieldsHTTPException,
    UncorrectHotelDataException,
    UncorrectHotelIDHTTPException,
    UncorrectRoomDataException,
    UncorrectRoomIDHTTPException,
    UncorrectincorrectFieldsException,
)
from src.api.dependecies import DBDep
from src.schemas.rooms import RoomAddRequest, RoomPATCHRequest


router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2025-08-30"),
    date_to: date = Query(example="2025-07-01"),
):
    try:
        return await RoomService(db).get_rooms(hotel_id, date_from, date_to)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except UncorrectHotelDataException:
        raise UncorrectHotelIDHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except UncorrectRoomDataException:
        raise UncorrectRoomIDHTTPException


@router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Room in hotel",
                "description": "Create a new room with the provided data.",
                "value": {
                    "title": "Lux",
                    "description": "cool room",
                    "price": 100,
                    "quantity": 2,
                    "facilities_ids": [1, 2],
                },
            },
            "2": {
                "summary": "Room in hotel",
                "description": "Create a new room with the provided data.",
                "value": {
                    "title": "Family",
                    "description": "family room",
                    "price": 150,
                    "quantity": 1,
                    "facilities_ids": [1, 2],
                },
            },
        }
    ),
):
    try:
        await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except ObjectAlreadyExistsException:
        raise RoomAlreadyExistsHTTPException
    except UncorrectHotelDataException:
        raise UncorrectHotelIDHTTPException
    except ForeinKeyViolationException:
        raise FacilitisNotExistsHTTPException
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    try:
        await RoomService(db).update_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except UncorrectHotelDataException:
        raise UncorrectHotelIDHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except UncorrectRoomDataException:
        raise UncorrectRoomIDHTTPException
    except ForeinKeyViolationException:
        raise FacilitisNotExistsHTTPException
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Patch hotel data",
    description="Update specific fields of a hotel record.",
)
async def patch_room(hotel_id: int, room_id: int, room_data: RoomPATCHRequest, db: DBDep):
    try:
        await RoomService(db).patch_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except UncorrectHotelDataException:
        raise UncorrectHotelIDHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except UncorrectRoomDataException:
        raise UncorrectRoomIDHTTPException
    except ForeinKeyViolationException:
        raise FacilitisNotExistsHTTPException
    except UncorrectincorrectFieldsException:
        raise UncorrectFieldsHTTPException
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except UncorrectHotelDataException:
        raise UncorrectHotelIDHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except UncorrectRoomDataException:
        raise UncorrectRoomIDHTTPException
    except ForeinKeyRoomViolationException:
        raise ForeignKeyViolationErrorHTTPException
    return {"status": "OK"}
