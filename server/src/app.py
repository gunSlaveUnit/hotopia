from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from settings import DEBUG
from core.utils.db import create as create_db
from server.src.api.v1.api import router as api_v1_router

app = FastAPI(debug=DEBUG)

app.include_router(api_v1_router)

app.mount("/media", StaticFiles(directory="media"), name="media")


@app.on_event("startup")
async def startup_event() -> None:
    await create_db()
