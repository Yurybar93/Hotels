import json
from pathlib import Path
import pytest

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.config import settings
from src.models import *
from src.main import app
from src.utils.db_manager import DBManager

from httpx import ASGITransport, AsyncClient


@pytest.fixture(scope="session", autouse=True)
async def check_database():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_database):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session", autouse=True)
def hotel_payload():
    return json.loads((Path(__file__).parent /"mock_hotels.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session", autouse=True)
async def add_data(setup_database, hotel_payload):
    with open("tests/mock_hotels.json", encoding="utf-8") as f_hotels:
        hotels = json.load(f_hotels)

    with open("tests/mock_rooms.json", encoding="utf-8") as f_hotels:
        rooms = json.load(f_hotels)
    
    hotels = [HotelAdd.model_validate(h) for h in hotels]
    rooms = [RoomAdd.model_validate(h) for h in rooms]

    async with DBManager(session_factory = async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)
        await db.commit()

    
            

        

@pytest.fixture(scope="session", autouse=True)
async def register_test_user(setup_database):
    transport=ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "first_name": "Max",
                "last_name": "Muster",
                "email": "muster@muster.com",
                "password": "1234"
            }
        )


