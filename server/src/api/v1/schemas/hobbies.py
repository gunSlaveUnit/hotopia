from pydantic import BaseModel

from server.src.api.v1.schemas.entity import EntityDBSchema


class HobbyBaseSchema(BaseModel):
    name: str
    short_description: str
    long_description: str


class HobbyCreateSchema(HobbyBaseSchema):
    pass


class HobbyDBSchema(HobbyCreateSchema, EntityDBSchema):
    class Config:
        from_attributes = True
