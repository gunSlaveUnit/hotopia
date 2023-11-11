from fastapi import APIRouter

from src.settings import API_VERSION_1_PREFIX

from src.api.v1.endpoints.hobbies import router as hobbies_router

router = APIRouter(prefix=API_VERSION_1_PREFIX)

router.include_router(hobbies_router)