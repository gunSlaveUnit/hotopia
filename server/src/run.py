import uvicorn

from core.settings import RELOAD
from common.src.core.settings import HOST, PORT

if __name__ == '__main__':
    uvicorn.run("app:app", host=HOST, port=PORT, reload=RELOAD)
