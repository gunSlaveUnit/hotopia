from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.entity import Entity

if TYPE_CHECKING:
    from core.models.modules import Module
    from core.models.walkthroughes import Walkthrough


class Unit(Entity):
    __tablename__ = "units"

    name: Mapped[str]
    experience_amount: Mapped[int]
    duration: Mapped[int]
    content_filename: Mapped[str]

    module_id: Mapped[int] = mapped_column("module_id", ForeignKey("modules.id"))
    previous_unit_id: Mapped[int] = mapped_column("unit_id", ForeignKey("units.id"), nullable=True)

    module: Mapped[Module] = relationship("Module", back_populates="units")
    walkthroughes: Mapped[list[Walkthrough]] = relationship("Walkthrough", back_populates="unit")
