from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models.entity import Entity


class Module(Entity):
    __tablename__ = "modules"

    name: Mapped[str]
    description: Mapped[str]

    hobby_id: Mapped[int] = mapped_column("hobby_id", ForeignKey("hobbies.id"))
    previous_module_id: Mapped[int] = mapped_column("module_id", ForeignKey("modules.id"), nullable=True)
