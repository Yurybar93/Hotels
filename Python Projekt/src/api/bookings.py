from fastapi import Body, HTTPException
from fastapi import APIRouter

from src.exceptions import AllRoomsBookedException, ObjectNotFoundException, UncorrectDataException
from src.api.dependecies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def create_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest = Body()):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Room not found")
    except UncorrectDataException as ex:
        raise HTTPException(status_code=400, detail=ex.detail)

    _booking_data = BookingAdd(**booking_data.model_dump(), user_id=user_id, price=room.price)
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
    except AllRoomsBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": booking}
