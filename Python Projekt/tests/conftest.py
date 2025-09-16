import pytest

from src.database import Base, engine_null_pool
from src.config import settings
from src.models import *

from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
async def check_database():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_database):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        

@pytest.fixture(scope="function", autouse=True)
async def register_test_user(setup_database):
    async with AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        await ac.post(
            "/auth/register",
            json={
                "first_name": "Max",
                "last_name": "Muster",
                "email": "muster@muster.com",
                "password": "1234"
            }
        )


