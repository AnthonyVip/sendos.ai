from fastapi import APIRouter, Body, Depends, HTTPException, status, Query
from typing import List, Union
from uuid import UUID

from db.repositories.inventory import InventoryRepository
from routes.dependencies.database import get_repository
from schemas.items import ItemPut, ItemResponse
from db.tables.items import ItemBase
from decorators.auth import get_current_user


router = APIRouter()


@router.get("/items", response_model=List[ItemResponse])
async def get_items(
    repository: InventoryRepository = Depends(
        get_repository(InventoryRepository)
    ),
    user: dict = Depends(get_current_user),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    return await repository.get_all(offset=offset, limit=limit)


@router.get("/items/{id}", response_model=ItemResponse)
async def get_item_by_id(
    id: Union[UUID, str],
    repository: InventoryRepository = Depends(
        get_repository(InventoryRepository)
    ),
    user: dict = Depends(get_current_user)
):
    item = await repository.get_by_id(id)

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return item


@router.put("/items/{id}", response_model=ItemResponse)
async def update_item(
    id: Union[UUID, str],
    item: ItemPut = Body(...),
    repository: InventoryRepository = Depends(
        get_repository(InventoryRepository)
    ),
    user: dict = Depends(get_current_user)
):
    item_db = await repository.update(id, item)

    if not item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return item_db


@router.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_item(
    item: ItemBase = Body(...),
    repository: InventoryRepository = Depends(
        get_repository(InventoryRepository)
    ),
    user: dict = Depends(get_current_user)
):
    return await repository.create(item)


@router.delete("/items/{id}", response_model=bool)
async def delete_item(
    id: Union[UUID, str],
    repository: InventoryRepository = Depends(
        get_repository(InventoryRepository)
    ),
    user: dict = Depends(get_current_user)
):
    return await repository.delete(id)
