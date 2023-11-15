from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.users import User
from core.utils.auth import verify_password

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return crypt_context.hash(password)


async def authenticate_user(
        db: AsyncSession,
        account_name: str,
        password: str
) -> Optional[User]:
    user = await User.by_account_name(db, account_name)
    if user and await verify_password(password, user.password):
        return user
    return None
