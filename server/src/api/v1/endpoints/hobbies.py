from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.db import get_db
from core.models.hobbies import Hobby
from server.src.settings import HOBBIES_ROUTER_PREFIX
from server.src.api.v1.schemas.hobbies import HobbyDBSchema, HobbyCreateSchema

router = APIRouter(prefix=HOBBIES_ROUTER_PREFIX)


@router.get('/', response_model=List[HobbyDBSchema])
async def items(db: AsyncSession = Depends(get_db)) -> List[Hobby]:
    return [_ async for _ in Hobby.every(db)]


@router.get('/{item_id}', response_model=Optional[HobbyDBSchema])
async def item(item_id: int, db: AsyncSession = Depends(get_db)) -> Optional[Hobby]:
    return await Hobby.by_id(db, item_id)


@router.post('/', response_model=HobbyDBSchema)
async def create(
        data: HobbyCreateSchema,
        db: AsyncSession = Depends(get_db)
) -> Hobby:
    return await Hobby.create(db, data)
