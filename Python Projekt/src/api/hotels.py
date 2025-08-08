from fastapi import Query, APIRouter, Body
from sqlalchemy import insert

from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependecies import PaginationDep
from src.database import async_session, engine
from src.models.hotels import HotelsOrm 
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
   


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session() as session:
        result = await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    
    return {"status": "OK"}


@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
        #add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        #print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        #await session.execute(add_hotel_stmt)
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session() as session:
        result = await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
      
    # global hotels
    # for hotel in hotels:
    #     if hotel["id"] == hotel_id:
    #         hotel["title"] = hotel_data.title
    #         hotel["name"] = hotel_data.name
        return {"status": "OK"}
        
@router.patch("/{hotel_id}")
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] =hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            return {"status": "OK"}