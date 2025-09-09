from datetime import date
from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.schemas.hotels import HotelAdd, HotelPATCH
from src.api.dependecies import DBDep, PaginationDep



router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Локация отеля"),
        date_from: date = Query(example="2025-08-30"),
        date_to: date = Query(example="2025-07-01")
        
):
    per_page = pagination.per_page or 5
    print(f"иду в бд")
    return await db.hotels.get_filtered_by_time(
        date_from = date_from,
        date_to = date_to,
        title=title,
        location=location,
        limit=per_page,
        offset=(pagination.page - 1) * per_page
    )
    
@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)
   

@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(openapi_examples={
        "1": {
            "summary": "Sochi", 
                "description": "Create a new hotel with the provided data.", 
                "value": 
                {"title": "Sochi 5", 
                "location": "sochi u morya",

            }
        },
        "2": {
            "summary": "Dubai", 
                "description": "Create a new hotel with the provided data.",
                "value": 
                {"title": "Dubai 5", 
                    "location": "dubai u morya",

            }           
                        
        }
    })
):
   
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, 
                       hotel_data: HotelAdd,
                       db: DBDep
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}
        
        
@router.patch("/{hotel_id}", 
              summary="Patch hotel data",
              description="Update specific fields of a hotel record."
)
async def patch_hotel(hotel_id: int, 
                      hotel_data: HotelPATCH,
                      db: DBDep
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
        