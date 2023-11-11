from fastapi import FastAPI

from server.src.api.v1.api import router as api_v1_router

app = FastAPI(debug=True)

app.include_router(api_v1_router)
