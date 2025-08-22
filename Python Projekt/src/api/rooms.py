from fastapi import APIRouter, Body

from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPATCH, RoomPATCHRequest
from src.database import async_session
from src.repositories.rooms import RoomsRepository



router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)
    
@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)
   

@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {"summary": "Room in hotel", 
          "description": "Create a new room with the provided data.", 
          "value": {"title": "Lux", "description": "cool room", "price": 100, "quantity": 2
        }
    },
    "2": {"summary": "Room in hotel", 
          "description": "Create a new room with the provided data.", 
          "value": {"title": "Family", "description": "family room", "price": 150, "quantity": 1
        }         
                    
    }
})):
    _room_data = RoomAdd(**room_data.model_dump(), hotel_id=hotel_id)
    async with async_session() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(**room_data.model_dump(), hotel_id=hotel_id)
    async with async_session() as session:
        await RoomsRepository(session).edit(_room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}
        
@router.patch("/{hotel_id}/rooms/{room_id}", 
              summary="Patch hotel data",
              description="Update specific fields of a hotel record."
)
async def patch_room(hotel_id: int, 
                     room_id: int,
                     room_data: RoomPATCHRequest
):  
    _room_data = RoomPATCH(**room_data.model_dump(), hotel_id=hotel_id)
    async with async_session() as session:
        await RoomsRepository(session).edit(_room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}


        