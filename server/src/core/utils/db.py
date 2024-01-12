import redis
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession, AsyncEngine

from server.src.core.settings import CONFIG

engine: AsyncEngine = create_async_engine(CONFIG['DB_URL'])


class Base(DeclarativeBase, AsyncAttrs):
    pass


async def get_db() -> AsyncSession:
    session_maker = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False
    )

    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_session_storage():
    storage = redis.asyncio.Redis()
    try:
        yield storage
    finally:
        await storage.aclose()
