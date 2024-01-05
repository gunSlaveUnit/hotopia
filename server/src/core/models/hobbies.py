from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from server.src.core.models.entity import Entity

if TYPE_CHECKING:
    from server.src.core.models.modules import Module


class Hobby(Entity):
    __tablename__ = "hobbies"

    name: Mapped[str]
    short_description: Mapped[str]
    long_description: Mapped[str]
    card_picture_filename: Mapped[str]

    modules: Mapped[list[Module]] = relationship("Module", back_populates="hobby")
