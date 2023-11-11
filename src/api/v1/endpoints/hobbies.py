from typing import List

from fastapi import APIRouter

from src.settings import HOBBIES_ROUTER_PREFIX
from src.api.v1.schemas.hobbies import HobbyBaseSchema, HobbyDBSchema

router = APIRouter(prefix=HOBBIES_ROUTER_PREFIX)


@router.get('/', response_model=List[HobbyBaseSchema])
async def items():
    return [
        {
            "id": 0,
            "created_at": 1699701695,
            "updated_at": None,
            "name": "Airsoft",
        },
        {
            "id": 1,
            "created_at": 1699701695,
            "updated_at": None,
            "name": "Card tricks",
        },
    ]


@router.get('/{item_id}', response_model=HobbyDBSchema)
async def item(item_id: int):
    return {
        "id": item_id,
        "created_at": 1699701695,
        "updated_at": None,
        "name": "some_hobby",
    }
