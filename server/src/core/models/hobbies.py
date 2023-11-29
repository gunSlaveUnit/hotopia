from sqlalchemy.orm import Mapped

from core.models.entity import Entity


class Hobby(Entity):
    __tablename__ = "hobbies"

    name: Mapped[str]
    short_description: Mapped[str]
