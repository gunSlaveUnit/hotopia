import sys

import uvicorn

from core.settings import BASE_PATH
sys.path.append(str(BASE_PATH))

from server.src.core.settings import HOST, PORT, RELOAD

if __name__ == '__main__':
    uvicorn.run("app:app", host=HOST, port=PORT, reload=RELOAD)
