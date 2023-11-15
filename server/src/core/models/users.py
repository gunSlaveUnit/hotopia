import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from core.models.entity import Entity


class User(Entity):
    __tablename__ = "users"

    email: Mapped[str]
    account_name: Mapped[str]
    displayed_name: Mapped[str]
    password: Mapped[str]
    is_active: Mapped[bool]
    login_at: Mapped[datetime.datetime] = mapped_column(server_default=None, nullable=True)

    @staticmethod
    async def by_email(session: AsyncSession, email: str) -> Optional:
        return await session.scalar(select(User).where(User.email == email))
