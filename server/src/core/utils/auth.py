from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from core.models.users import User
from core.utils.crypt import crypt_context


async def verify_password(plain_password, hashed_password) -> bool:
    return crypt_context.verify(plain_password, hashed_password)


async def authenticate_user(
        db: AsyncSession,
        account_name: str,
        password: str
) -> Optional[User]:
    user = await User.by_account_name(db, account_name)
    if user and await verify_password(password, user.password):
        return user
    return None
