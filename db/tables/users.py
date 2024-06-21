from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import String
from sqlmodel import Column, Field, SQLModel

from db.tables.base import UUIDModel, TimeStampedModel


class UserBase(SQLModel):
    email: EmailStr = Field(sa_column=Column("email", String, unique=True))


class User(UserBase, UUIDModel, TimeStampedModel, table=True):
    status: str = Field(default="active")
    password: Optional[bytes] = None
    last_login: Optional[datetime] = None

    __tablename__ = "users"
