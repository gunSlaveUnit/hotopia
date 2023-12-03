from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from core.utils.db import create as create_db
from settings import DEBUG, MEDIA_PATH, MEDIA_PREFIX
from server.src.api.v1.api import router as api_v1_router

app = FastAPI(debug=DEBUG)

app.include_router(api_v1_router)

if DEBUG:
    app.mount(MEDIA_PREFIX, StaticFiles(directory=MEDIA_PATH), name=MEDIA_PATH)


@app.on_event("startup")
async def startup_event() -> None:
    await create_db()
