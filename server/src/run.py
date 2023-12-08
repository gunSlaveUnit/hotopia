import uvicorn

from settings import HOST, PORT

if __name__ == '__main__':
    uvicorn.run("app:app", host=HOST, port=PORT, reload=True)
