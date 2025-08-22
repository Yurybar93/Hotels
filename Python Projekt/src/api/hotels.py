from fastapi import Query, APIRouter, Body

from src.schemas.hotels import HotelAdd, HotelPATCH
from src.api.dependecies import PaginationDep
from src.database import async_session
from src.repositories.hotels import HotelsRepository



router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Локация отеля"),
        
):
    per_page = pagination.per_page or 5
    async with async_session() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=(pagination.page - 1) * per_page
        )
    
@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)
   


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.post("")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": "Sochi", 
          "description": "Create a new hotel with the provided data.", 
          "value": {"title": "Sochi 5", "location": "sochi u morya",
        }
    },
    "2": {"summary": "Dubai", 
          "description": "Create a new hotel with the provided data.",
            "value": {"title": "Dubai 5", "location": "dubai u morya",
            }           
                    
    }
})):
   
    async with async_session() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}
        
@router.patch("/{hotel_id}", 
              summary="Patch hotel data",
              description="Update specific fields of a hotel record."
)
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


        