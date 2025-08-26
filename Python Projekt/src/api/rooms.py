from datetime import date
from fastapi import APIRouter, Body, Query

from src.api.dependecies import DBDep
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPATCH, RoomPATCHRequest




router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int, 
        db: DBDep,
        date_from: date = Query(example="2025-08-30"),
        date_to: date = Query(example="2025-07-01")
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

    
@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
        hotel_id: int, 
        room_id: int,
        db: DBDep
):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
   

@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, 
                      room_id: int,
                      db: DBDep
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, 
                      db: DBDep,
                      room_data: RoomAddRequest = Body(openapi_examples={
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
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(hotel_id: int, 
                      room_id: int, 
                      room_data: RoomAddRequest,
                      db: DBDep
):
    _room_data = RoomAdd(**room_data.model_dump(), hotel_id=hotel_id)
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
    return {"status": "OK"}

        
@router.patch("/{hotel_id}/rooms/{room_id}", 
              summary="Patch hotel data",
              description="Update specific fields of a hotel record."
)
async def patch_room(hotel_id: int, 
                     room_id: int,
                     room_data: RoomPATCHRequest,
                     db: DBDep
):  
    _room_data = RoomPATCH(**room_data.model_dump(exclude_unset=True), hotel_id=hotel_id)
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


        