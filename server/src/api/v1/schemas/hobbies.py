from pydantic import BaseModel

from server.src.api.v1.schemas.entity import EntityDBSchema


class HobbyBaseSchema(BaseModel):
    name: str


class HobbyDBSchema(HobbyBaseSchema, EntityDBSchema):
    class Config:
        from_attributes = True
