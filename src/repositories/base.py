import logging
from typing import Sequence, Any

from asyncpg import ForeignKeyViolationError
from pydantic import BaseModel

from asyncpg.exceptions import UniqueViolationError, DataError
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound, DBAPIError, IntegrityError
from src.exceptions import (
    ForeinKeyViolationException,
    ObjectNotFoundException,
    UncorrectDataException,
    ObjectAlreadyExistsException,
)
from src.repositories.mappers.base import DataMapper
from src.database import engine


class BaseRepository:
    model = None
    mapper = DataMapper

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by) -> list[BaseModel | Any]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs) -> list[BaseModel | Any]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by) -> BaseModel | None | Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        try:
            result = await self.session.execute(query)
            model = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        except DBAPIError:
            raise UncorrectDataException
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel) -> BaseModel | Any:
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            model = await self.session.execute(add_stmt)
            print(add_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
            model = model.scalars().one()
        except IntegrityError as ex:
            logging.error(f"Unable to add data: {data}.")
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            logging.error(f"Unknown error: {type(ex.orig.__cause__)=}")
            raise ex
        except DBAPIError:
            raise UncorrectDataException
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: Sequence[BaseModel]) -> None:
        try:
            add_stmt = insert(self.model).values([item.model_dump() for item in data])
            await self.session.execute(add_stmt)
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                raise ForeinKeyViolationException from ex
            raise ex

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        try:
            smt_check = select(self.model).filter_by(**filter_by)
            result = await self.session.execute(smt_check)
            obj = result.scalars().all()
            if not obj:
                raise ObjectNotFoundException

            edit_stmt = (
                update(self.model)
                .filter_by(**filter_by)
                .values(**data.model_dump(exclude_unset=exclude_unset))
            )
            await self.session.execute(edit_stmt)

        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                raise ForeinKeyViolationException
        except DBAPIError as ex:
            if isinstance(ex.orig.__cause__, DataError):
                raise UncorrectDataException
            raise ex

        print(edit_stmt.compile(self.session.bind, compile_kwargs={"literal_binds": True}))

    async def delete(self, **filter_by) -> None:
        try:
            smt_check = select(self.model).filter_by(**filter_by)
            result = await self.session.execute(smt_check)
            obj = result.scalars().all()

            if not obj:
                raise ObjectNotFoundException
            delete_stmt = delete(self.model).filter_by(**filter_by)
            await self.session.execute(delete_stmt)

        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                raise ForeinKeyViolationException
            raise ex
        except DBAPIError:
            raise UncorrectDataException
        print(delete_stmt.compile(self.session.bind, compile_kwargs={"literal_binds": True}))
