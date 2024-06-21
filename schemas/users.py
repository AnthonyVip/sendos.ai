from pydantic import BaseModel
from uuid import UUID
from typing import Union
from db.tables.users import UserBase


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: Union[UUID, str]


class UserResponse(BaseModel):
    jwt_token: str
