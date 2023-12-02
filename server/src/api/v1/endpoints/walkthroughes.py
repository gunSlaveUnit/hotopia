from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.db import get_db
from core.models.walkthroughes import Walkthrough
from server.src.settings import WALKTHROUGHES_ROUTER_PREFIX
from api.v1.schemas.walkthroughes import WalkthroughDBSchema, WalkthroughCreateSchema

router = APIRouter(prefix=WALKTHROUGHES_ROUTER_PREFIX)


@router.post('/', response_model=WalkthroughDBSchema)
async def create(data: WalkthroughCreateSchema, db: AsyncSession = Depends(get_db)):
    return await Walkthrough.create(db, data)
