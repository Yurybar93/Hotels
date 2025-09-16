

from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager
from src.database import async_session


async def test_add_hotel():
    hotel_data = HotelAdd(title="Test Hotel", location="Test Location", description="Test Description")
    async with DBManager(session_factory = async_session) as db:
        await db.hotels.add(hotel_data)
        await db.commit()