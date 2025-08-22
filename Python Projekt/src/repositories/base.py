from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from src.database import engine


class BaseRepository:
   model = None
   schema: BaseModel = None

   def __init__(self, session):
        self.session = session

   async def get_filtered(self, **filter_by):
       query = select(self.model).filter_by(**filter_by)
       result = await self.session.execute(query)
       print(query.compile(compile_kwargs={"literal_binds": True}))
       return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
        

   async def get_all(self,*args, **kwargs):
        return await self.get_filtered()
   
   async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)
   
   async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        model = await self.session.execute(add_stmt)
        print(add_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        model = model.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

   async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
       smt_check = select(self.model).filter_by(**filter_by)
       result = await self.session.execute(smt_check)
       obj = result.scalars().all()

       if not obj:
           raise HTTPException(status_code=404, detail="Object not found")
       if len(obj) > 1:
           raise HTTPException(status_code=400, detail="Multiple objects found")
       
       edit_stmt = (
           update(self.model)
           .filter_by(**filter_by)
           .values(**data.model_dump(exclude_unset=exclude_unset))
       )
       await self.session.execute(edit_stmt)
       print(edit_stmt.compile(self.session.bind, compile_kwargs={"literal_binds": True}))

   async def delete(self, **filter_by) -> None:
       smt_check = select(self.model).filter_by(**filter_by)
       result = await self.session.execute(smt_check)
       obj = result.scalars().all()

       if not obj:
           raise HTTPException(status_code=404, detail="Object not found")
       if len(obj) > 1:
           raise HTTPException(status_code=400, detail="Multiple objects found")
       
       delete_stmt = delete(self.model).filter_by(**filter_by)
       await self.session.execute(delete_stmt)
       print(delete_stmt.compile(self.session.bind, compile_kwargs={"literal_binds": True}))
