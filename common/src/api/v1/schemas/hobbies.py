from pydantic import BaseModel

from common.src.api.v1.schemas.entity import EntityDBSchema


class HobbyBaseSchema(BaseModel):
    name: str
    short_description: str
    long_description: str
    card_picture_filename: str


class HobbyCreateSchema(HobbyBaseSchema):
    pass


class HobbyDBSchema(HobbyCreateSchema, EntityDBSchema):
    class Config:
        from_attributes = True
