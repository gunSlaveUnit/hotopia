from pydantic import BaseModel

from common.src.api.v1.schemas.entity import EntityDBSchema


class UnitBaseSchema(BaseModel):
    name: str
    experience_amount: int
    duration: int
    content_filename: str
    module_id: int
    previous_unit_id: int | None


class UnitCreateSchema(UnitBaseSchema):
    pass


class UnitDBSchema(UnitCreateSchema, EntityDBSchema):
    class Config:
        from_attributes = True
