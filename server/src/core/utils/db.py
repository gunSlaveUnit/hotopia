from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

engine: AsyncEngine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@localhost:5432/hotopia"
)
