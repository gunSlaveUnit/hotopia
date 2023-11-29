from pydantic import BaseModel

from server.src.api.v1.schemas.entity import EntityDBSchema


class UnitBaseSchema(BaseModel):
    name: str
    done: bool
    experience_amount: int
    duration: int
    module_id: int
    previous_unit_id: int | None


class UnitCreateSchema(UnitBaseSchema):
    pass


class UnitDBSchema(UnitCreateSchema, EntityDBSchema):
    class Config:
        from_attributes = True
