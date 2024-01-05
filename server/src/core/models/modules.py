from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.src.core.models.entity import Entity

if TYPE_CHECKING:
    from server.src.core.models.units import Unit
    from server.src.core.models.hobbies import Hobby


class Module(Entity):
    __tablename__ = "modules"

    name: Mapped[str]
    description: Mapped[str]

    hobby_id: Mapped[int] = mapped_column("hobby_id", ForeignKey("hobbies.id"))
    previous_module_id: Mapped[int] = mapped_column("module_id", ForeignKey("modules.id"), nullable=True)

    hobby: Mapped[Hobby] = relationship("Hobby", back_populates="modules")
    units: Mapped[list[Unit]] = relationship("Unit", back_populates="module")
