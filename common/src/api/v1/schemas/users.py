import datetime

from pydantic import BaseModel, EmailStr

from common.src.api.v1.schemas.entity import EntityDBSchema


class UserSignInSchema(BaseModel):
    password: str
    account_name: str


class UserSignUpSchema(UserSignInSchema):
    email: EmailStr


class UserDBSchema(EntityDBSchema, UserSignUpSchema):
    is_active: bool
    displayed_name: str
    login_at: datetime.datetime | None
