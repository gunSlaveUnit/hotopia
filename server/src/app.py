from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from server.src.core.utils.db import create as create_db
from server.src.api.v1.api import router as api_v1_router
from server.src.core.settings import CONFIG, MEDIA_PREFIX, MEDIA_PATH

debug = CONFIG['DEBUG']
app = FastAPI(debug=debug)
if debug:
    app.mount(MEDIA_PREFIX, StaticFiles(directory=MEDIA_PATH), name=MEDIA_PATH)

app.include_router(api_v1_router)


@app.on_event("startup")
async def startup_event() -> None:
    await create_db()
