from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel import Session, create_engine, select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Union

from core.settings import settings
from db.tables.items import Item
from schemas.items import ItemPut, ItemResponse


engine = create_engine(settings.database_url, echo=True)


class InventoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self,
        offset: int = 0,
        limit: int = 100,
    ) -> List[ItemResponse]:
        query = select(Item).where(Item.status == "active").offset(offset).limit(limit)

        results = await self.session.exec(query)

        return results.all()

    async def get_by_id(self, id: Union[UUID, str]) -> ItemResponse:
        item = await self.session.get(Item, id)

        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return item

    async def create(self, item: Item) -> ItemResponse:
        item_db = Item.model_validate(item)

        self.session.add(item_db)
        await self.session.commit()
        await self.session.refresh(item_db)

        return item_db

    async def update(self, id: Union[UUID, str], item: ItemPut) -> ItemResponse:
        item_db = await self.session.get(Item, id)

        if not item_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        item_data = item.model_dump(exclude_unset=True)
        for key, value in item_data.items():
            setattr(item_db, key, value)

        self.session.add(item_db)
        await self.session.commit()
        await self.session.refresh(item_db)

        return item_db

    async def delete(self, id: Union[UUID, str]) -> bool:
        item = await self.session.get(Item, id)

        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        item.status = "deleted"
        self.session.add(item)
        await self.session.commit()

        return True
