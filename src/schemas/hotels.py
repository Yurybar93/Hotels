from pydantic import BaseModel, constr, model_validator


class HotelAdd(BaseModel):
    title: constr(min_length=1, max_length=100)
    location: constr(min_length=1, max_length=100)


class Hotel(HotelAdd):
    id: int


class HotelPATCH(BaseModel):
    title: constr(min_length=1, max_length=100) | None = None
    location: constr(min_length=1, max_length=100) | None = None

    @model_validator(mode="after")
    def at_least_one_field(self):
        if not self.model_dump(exclude_none=True):
            raise ValueError("The request body must contain at least one field.")
        return self
