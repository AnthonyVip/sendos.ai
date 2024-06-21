from pydantic import condecimal
from sqlmodel import Field, SQLModel
from db.tables.base import UUIDModel, TimeStampedModel


class ItemBase(SQLModel):
    name: str = Field(nullable=False)
    description: str = Field(nullable=True)
    quantity: int = Field(nullable=False, default=0)
    price: condecimal(decimal_places=2) = Field(default=0)


class Item(ItemBase, UUIDModel, TimeStampedModel, table=True):
    status: str = Field(default="active")
    __tablename__ = "items"
