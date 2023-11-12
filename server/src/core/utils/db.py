from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

engine: AsyncEngine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@localhost:5432/hotopia"
)


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
