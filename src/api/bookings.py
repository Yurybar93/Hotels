from fastapi import Body
from fastapi import APIRouter

from services.bookings import BookingService
from src.api.dependecies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("")
async def create_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest = Body()):
    booking = await BookingService(db).add_booking(booking_data, user_id)
    return {"status": "OK", "data": booking}
