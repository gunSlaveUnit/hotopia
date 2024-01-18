#!/usr/bin/env python3

import uvicorn

from server.src.core.settings import CONFIG


if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        host=CONFIG["HOST"],
        port=int(CONFIG["PORT"]),
        reload=bool(CONFIG["RELOAD"]),
    )
