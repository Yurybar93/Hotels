from sqlalchemy import select
from schemas.hotels import Hotel
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm

class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self, 
                      title,
                      location,
                      limit,
                      offset
    ) -> list[Hotel]:
        query = select(HotelsOrm)
        if title:
            query = query.where(HotelsOrm.title.ilike(f"%{title}%"))
        if location:
            query = query.where(HotelsOrm.location.ilike(f"%{location}%"))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
       