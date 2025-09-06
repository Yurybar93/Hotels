from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.init import redis_connector
from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_connector.connect()
    print("Connected to Redis")
    yield
    await redis_connector.close()
    print("Disconnected from Redis")

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(hotels_router)   
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)
    

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)