from fastapi import APIRouter

from settings import HOBBIES_ROUTER_PREFIX

router = APIRouter(prefix=HOBBIES_ROUTER_PREFIX)


@router.get('/')
async def items():
    return [
        {
            "id": 0,
            "name": "Strikeball",
        },
        {
            "id": 1,
            "name": "Card tricks",
        },
    ]
