import uvicorn

from settings import RELOAD
from common.src.settings import HOST, PORT

if __name__ == '__main__':
    uvicorn.run("app:app", host=HOST, port=PORT, reload=RELOAD)
