from typing import List

from fastapi import APIRouter

from server.src.api.v1.schemas.hobbies import HobbyDBSchema
from server.src.settings import HOBBIES_ROUTER_PREFIX

router = APIRouter(prefix=HOBBIES_ROUTER_PREFIX)


@router.get('/', response_model=List[HobbyDBSchema])
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
