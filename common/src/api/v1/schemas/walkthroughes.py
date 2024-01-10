from pydantic import BaseModel

from common.src.api.v1.schemas.entity import EntityDBSchema


class WalkthroughBaseSchema(BaseModel):
    user_id: int
    unit_id: int


class WalkthroughCreateSchema(WalkthroughBaseSchema):
    pass


class WalkthroughDBSchema(WalkthroughCreateSchema, EntityDBSchema):
    class Config:
        from_attributes = True
