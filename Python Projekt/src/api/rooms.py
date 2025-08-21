from fastapi import Query, APIRouter, Body

from schemas.rooms import RoomAdd, RoomPATCH
from src.schemas.hotels import HotelAdd, HotelPATCH
from src.api.dependecies import PaginationDep
from src.database import async_session
from src.repositories.rooms import RoomsRepository



router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id)
   


@router.delete("/{hotel_id}/{room_id}")
async def delete_room(room_id: int):
    async with async_session() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.post("/{hotel_id}")
async def create_room(room_data: RoomAdd = Body(openapi_examples={
    "1": {"summary": "Room in hotel", 
          "description": "Create a new room with the provided data.", 
          "value": {"hotel_id": 1, "title": "Lux", "description": "cool room", "price": 100, "quantity": 2
        }
    },
    "2": {"summary": "Room in hotel", 
          "description": "Create a new room with the provided data.", 
          "value": {"hotel_id": 2, "title": "Family", "description": "family room", "price": 150, "quantity": 1
        }         
                    
    }
})):
    async with async_session() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/{room_id}")
async def update_room(room_id: int, room_data: RoomAdd):
    async with async_session() as session:
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}
        
@router.patch("/{hotel_id}/{room_id}", 
              summary="Patch hotel data",
              description="Update specific fields of a hotel record."
)
async def patch_room(room_id: int, room_data: RoomPATCH):
    async with async_session() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}

@router.get("/{hotel_id}/{room_id}")
async def get_room(room_id: int):
    async with async_session() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)
        