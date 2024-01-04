from fastapi import APIRouter

from common.src.settings import API_VERSION_1_PREFIX
from server.src.api.v1.endpoints.auth import router as auth_router
from server.src.api.v1.endpoints.units import router as units_router
from server.src.api.v1.endpoints.modules import router as modules_router
from server.src.api.v1.endpoints.hobbies import router as hobbies_router
from server.src.api.v1.endpoints.walkthroughes import router as walkthroughes_router

router = APIRouter(prefix=API_VERSION_1_PREFIX)

router.include_router(auth_router)
router.include_router(units_router)
router.include_router(modules_router)
router.include_router(hobbies_router)
router.include_router(walkthroughes_router)
