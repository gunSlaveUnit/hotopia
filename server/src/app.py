from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from server.src.core.settings import MEDIA_PREFIX
from server.src.core.settings import DEBUG, MEDIA_PATH
from server.src.core.utils.db import create as create_db
from server.src.api.v1.api import router as api_v1_router

app = FastAPI(debug=DEBUG)

app.include_router(api_v1_router)

if DEBUG:
    app.mount(MEDIA_PREFIX, StaticFiles(directory=MEDIA_PATH), name=MEDIA_PATH)


@app.on_event("startup")
async def startup_event() -> None:
    await create_db()
