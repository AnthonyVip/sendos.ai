from pydantic import BaseModel
from typing import Optional, Union
from uuid import UUID


class ItemPut(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None


class ItemResponse(BaseModel):
    id: Union[UUID, str]
    name: str
    description: str
    quantity: int
    price: float
