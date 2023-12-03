from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models.entity import Entity


class Unit(Entity):
    __tablename__ = "units"

    name: Mapped[str]
    done: Mapped[bool]
    experience_amount: Mapped[int]
    duration: Mapped[int]
    filename: Mapped[str]

    module_id: Mapped[int] = mapped_column("module_id", ForeignKey("modules.id"))
    previous_unit_id: Mapped[int] = mapped_column("unit_id", ForeignKey("units.id"), nullable=True)
