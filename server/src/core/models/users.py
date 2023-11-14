import datetime

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
