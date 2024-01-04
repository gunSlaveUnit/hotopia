from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.db import get_db
from core.models.walkthroughes import Walkthrough
from common.src.core.settings import WALKTHROUGHES_ROUTER_PREFIX
from common.src.api.v1.schemas.walkthroughes import WalkthroughDBSchema, WalkthroughCreateSchema

router = APIRouter(prefix=WALKTHROUGHES_ROUTER_PREFIX)


@router.get('', response_model=List[WalkthroughDBSchema])
async def items(
        user_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        db: AsyncSession = Depends(get_db)
) -> List[Walkthrough]:
    walkthroughes = Walkthrough.every(db)

    if user_id:
        walkthroughes = (walkthrough async for walkthrough in walkthroughes if walkthrough.user_id == user_id)

    if unit_id:
        walkthroughes = (walkthrough async for walkthrough in walkthroughes if walkthrough.unit_id == unit_id)

    return [_ async for _ in walkthroughes]


@router.post('', response_model=WalkthroughDBSchema)
async def create(data: WalkthroughCreateSchema, db: AsyncSession = Depends(get_db)):
    return await Walkthrough.create(db, data)


@router.delete('/{item_id}')
async def delete(item_id: int, db: AsyncSession = Depends(get_db)):
    return await Walkthrough.delete(db, item_id)
