from typing import List, Optional, AsyncIterator

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.db import get_db
from core.models.modules import Module
from server.src.settings import MODULES_ROUTER_PREFIX
from api.v1.schemas.modules import ModuleDBSchema, ModuleCreateSchema

router = APIRouter(prefix=MODULES_ROUTER_PREFIX)


@router.get('/', response_model=List[ModuleDBSchema])
async def items(
        hobby_id: Optional[int] = None,
        db: AsyncSession = Depends(get_db)
) -> List[Module]:
    hobbies = Module.every(db)

    if hobby_id:
        hobbies = (hobby async for hobby in hobbies if hobby.hobby_id == hobby_id)

    return [_ async for _ in hobbies]


@router.post('/', response_model=ModuleDBSchema)
async def create(data: ModuleCreateSchema, db: AsyncSession = Depends(get_db)):
    return await Module.create(db, data)
