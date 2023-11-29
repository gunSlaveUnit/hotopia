from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.db import get_db
from core.models.units import Unit
from server.src.settings import UNITS_ROUTER_PREFIX
from api.v1.schemas.units import UnitDBSchema, UnitCreateSchema

router = APIRouter(prefix=UNITS_ROUTER_PREFIX)


@router.get('/', response_model=List[UnitDBSchema])
async def items(db: AsyncSession = Depends(get_db)) -> List[Unit]:
    return [_ async for _ in Unit.every(db)]


@router.post('/', response_model=UnitDBSchema)
async def create(data: UnitCreateSchema, db: AsyncSession = Depends(get_db)):
    return await Unit.create(db, data)
