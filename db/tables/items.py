import uuid
from datetime import datetime
from pydantic import BaseModel, condecimal
from sqlmodel import Field, SQLModel


class UUIDModel(BaseModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )


class TimeStampedModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ItemBase(SQLModel):
    name: str = Field(nullable=False)
    description: str = Field(nullable=True)
    quantity: int = Field(nullable=False, default=0)
    price: condecimal(decimal_places=2) = Field(default=0)


class Item(ItemBase, UUIDModel, TimeStampedModel, table=True):
    status: str = Field(default="active")
    __tablename__ = "items"
