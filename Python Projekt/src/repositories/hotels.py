from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm

class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self, 
                      title,
                      location,
                      limit,
                      offset
    ):
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
        return result.scalars().all()
       