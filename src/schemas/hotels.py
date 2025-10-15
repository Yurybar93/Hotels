from pydantic import BaseModel, constr


class HotelAdd(BaseModel):
    title: constr(min_length=1, max_length=100)
    location: constr(min_length=1, max_length=100)


class Hotel(HotelAdd):
    id: int


class HotelPATCH(BaseModel):
    title: constr(min_length=1, max_length=100) | None = None
    location: constr(min_length=1, max_length=100) | None = None
