from pydantic import BaseModel

class Hotel(BaseModel):
    id: int
    title: str
    name: str

class HotelPATCH(BaseModel):
    title: str | None = None
    name: str | None = None