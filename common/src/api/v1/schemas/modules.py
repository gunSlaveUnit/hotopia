from pydantic import BaseModel

from common.src.api.v1.schemas.entity import EntityDBSchema


class ModuleBaseSchema(BaseModel):
    name: str
    description: str
    hobby_id: int
    previous_module_id: int | None


class ModuleCreateSchema(ModuleBaseSchema):
    pass


class ModuleDBSchema(ModuleCreateSchema, EntityDBSchema):
    class Config:
        from_attributes = True
