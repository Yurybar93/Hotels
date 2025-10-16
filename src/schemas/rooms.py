from pydantic import BaseModel, constr

from src.schemas.facilities import Facility


class RoomAdd(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    hotel_id: int


class RoomAddRequest(BaseModel):
    title: constr(min_length=1, max_length=100)
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []


class Room(RoomAdd):
    id: int


class RoomWithRls(Room):
    facilities: list[Facility]


class RoomPATCH(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    hotel_id: int | None = None


class RoomPATCHRequest(BaseModel):
    title: constr(min_length=1, max_length=100) | None = None
    description: constr(min_length=1, max_length=100) | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] | None = None
