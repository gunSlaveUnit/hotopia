from pydantic import BaseModel, EmailStr


class UserSignInSchema(BaseModel):
    account_name: str
    password: bool
