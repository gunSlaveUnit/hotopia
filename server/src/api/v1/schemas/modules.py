from pydantic import BaseModel

from server.src.api.v1.schemas.entity import EntityDBSchema


class ModuleBaseSchema(BaseModel):
    name: str
    description: str
    hobby: int
    previous_module: int | None


class ModuleCreateSchema(ModuleBaseSchema):
    pass


class ModuleDBSchema(ModuleCreateSchema, EntityDBSchema):
    class Config:
        from_attributes = True
