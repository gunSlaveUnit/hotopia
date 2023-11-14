from pydantic import BaseModel

from server.src.api.v1.schemas.entity import EntityDBSchema


class UnitBaseSchema(BaseModel):
    name: str
    done: bool
    experience_amount: int
    module: int
    previous_unit: int | None


class UnitCreateSchema(UnitBaseSchema):
    pass


class UnitDBSchema(UnitCreateSchema, EntityDBSchema):
    class Config:
        from_attributes = True
