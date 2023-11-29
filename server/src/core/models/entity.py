import datetime
from typing import AsyncIterator, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from core.utils.db import Base


class Entity(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=None, onupdate=func.now(), nullable=True)

    @classmethod
    async def every(cls, session: AsyncSession) -> AsyncIterator:
        scalars = await session.stream_scalars(select(cls))
        async for scalar in scalars:
            yield scalar

    @classmethod
    async def by_id(cls, session: AsyncSession, item_id: int) -> Optional:
        return await session.scalar(select(cls).where(cls.id == item_id))

    @classmethod
    async def create(cls, session: AsyncSession, data):
        item = cls(**data.dict())

        session.add(item)
        await session.commit()
        await session.flush()

        return item

    async def update(self, session: AsyncSession, data):
        for attribute, value in data.items():
            if hasattr(self, attribute):
                setattr(self, attribute, value)
            else:
                raise AttributeError("The attribute to update does not exist in the source object")

        await session.commit()
        return await session.refresh(self)

    def dict(self) -> dict:
        """
        Model attributes excluding SQLAlchemy attributes
        :return: dict without SQLAlchemy attributes
        """
        return {k: v for (k, v) in self.__dict__.items() if '_sa_' != k[:4]}
