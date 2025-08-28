from fastapi import Body, HTTPException, Query
from fastapi import APIRouter

from src.api.dependecies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(
    user_id: UserIdDep,
    db: DBDep
):
    return await db.bookings.get_filtered(user_id=user_id)

@router.post("")
async def create_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body()
):
    
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    _booking_data = BookingAdd(**booking_data.model_dump(), user_id=user_id, price=room.price)
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}