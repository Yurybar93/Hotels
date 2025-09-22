from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestAdd(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserWithHashedPasswort(User):
    hashed_password: str
