from pydantic import BaseModel

from server.src.api.v1.schemas.entity import EntityDBSchema


class WalkthroughBaseSchema(BaseModel):
    user: int
    unit: int


class WalkthroughCreateSchema(WalkthroughBaseSchema):
    pass


class WalkthroughDBSchema(WalkthroughCreateSchema, EntityDBSchema):
    class Config:
        from_attributes = True
