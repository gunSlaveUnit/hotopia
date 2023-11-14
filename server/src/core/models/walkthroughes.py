from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models.entity import Entity


class Walkthrough(Entity):
    __tablename__ = "walkthroughes"

    user: Mapped[int] = mapped_column("user_id", ForeignKey("users.id"))
    unit: Mapped[int] = mapped_column("unit_id", ForeignKey("units.id"))
    done: Mapped[bool]
