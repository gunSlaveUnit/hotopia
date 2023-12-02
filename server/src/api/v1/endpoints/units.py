from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.db import get_db
from core.models.units import Unit
from server.src.settings import UNITS_ROUTER_PREFIX
from api.v1.schemas.units import UnitDBSchema, UnitCreateSchema

router = APIRouter(prefix=UNITS_ROUTER_PREFIX)


@router.get('/', response_model=List[UnitDBSchema])
async def items(
        module_id: Optional[int] = None,
        db: AsyncSession = Depends(get_db)
) -> List[Unit]:
    units = Unit.every(db)

    if module_id:
        units = (unit async for unit in units if unit.module_id == module_id)

    return [_ async for _ in units]


@router.post('/', response_model=UnitDBSchema)
async def create(data: UnitCreateSchema, db: AsyncSession = Depends(get_db)):
    return await Unit.create(db, data)
