from datetime import date
from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.exceptions import (
    ForeinKeyViolationException,
    HotelAlreadyExistsException,
    HotelAlreadyExistsHTTPException,
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
    UncorrectDataException,
    UncorrectFieldsHTTPException,
    UncorrectHotelIDHTTPException,
    ForeignKeyViolationErrorHTTPException,
    UncorrectincorrectFieldsException,
)
from src.schemas.hotels import HotelAdd, HotelPATCH
from src.api.dependecies import DBDep, PaginationDep
from src.services.hotels import HotelService


router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Локация отеля"),
    date_from: date = Query(example="2025-08-30"),
    date_to: date = Query(example="2025-07-01"),
):
    return await HotelService(db).get_hotels(
        pagination,
        title,
        location,
        date_from,
        date_to,
    )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    except UncorrectDataException:
        raise UncorrectHotelIDHTTPException


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Sochi",
                "description": "Create a new hotel with the provided data.",
                "value": {
                    "title": "Sochi 5",
                    "location": "sochi u morya",
                },
            },
            "2": {
                "summary": "Dubai",
                "description": "Create a new hotel with the provided data.",
                "value": {
                    "title": "Dubai 5",
                    "location": "dubai u morya",
                },
            },
        }
    ),
):
    try:
        hotel = await HotelService(db).create_hotel(hotel_data)
        return {"status": "OK", "data": hotel}
    except HotelAlreadyExistsException:
        raise HotelAlreadyExistsHTTPException


@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    try:
        await HotelService(db).update_hotel(hotel_id, hotel_data)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    except UncorrectDataException:
        raise UncorrectHotelIDHTTPException
    except UncorrectincorrectFieldsException:
        raise UncorrectFieldsHTTPException
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Patch hotel data",
    description="Update specific fields of a hotel record.",
)
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    try:
        await HotelService(db).patch_hotel(hotel_id, hotel_data)
        return {"status": "OK"}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    except UncorrectDataException:
        raise UncorrectHotelIDHTTPException
    except UncorrectincorrectFieldsException:
        raise UncorrectFieldsHTTPException


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    try:
        await HotelService(db).delete_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    except UncorrectDataException:
        raise UncorrectHotelIDHTTPException
    except ForeinKeyViolationException:
        raise ForeignKeyViolationErrorHTTPException
    return {"status": "OK"}
