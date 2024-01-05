from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.src.core.models.entity import Entity

if TYPE_CHECKING:
    from server.src.core.models.units import Unit


class Walkthrough(Entity):
    __tablename__ = "walkthroughes"

    user_id: Mapped[int] = mapped_column("user_id", ForeignKey("users.id"))
    unit_id: Mapped[int] = mapped_column("unit_id", ForeignKey("units.id"))

    unit: Mapped[Unit] = relationship("Unit", back_populates="walkthroughes")
