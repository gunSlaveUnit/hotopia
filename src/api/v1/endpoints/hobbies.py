from fastapi import APIRouter

from src.settings import HOBBIES_ROUTER_PREFIX

router = APIRouter(prefix=HOBBIES_ROUTER_PREFIX)


@router.get('/')
async def items():
    return [
        {
            "id": 0,
            "name": "Airsoft",
        },
        {
            "id": 1,
            "name": "Card tricks",
        },
    ]
