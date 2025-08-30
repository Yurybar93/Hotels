from pydantic import BaseModel

class RoomAdd(BaseModel):
    title: str
    description: str| None = None
    price: int
    quantity: int
    hotel_id: int

class RoomAddRequest(BaseModel):
    title: str 
    description: str| None = None
    price: int 
    quantity: int 
    facilities_ids: list[int] = []

class Room(RoomAdd):
    id: int

class RoomPATCH(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    hotel_id: int | None = None


class RoomPATCHRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] | None = None