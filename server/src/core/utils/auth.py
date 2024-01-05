from typing import Optional

from fastapi import HTTPException, Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from server.src.core.models.users import User
from server.src.core.utils.crypt import crypt_context
from server.src.core.utils.db import get_db, get_session_storage


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


async def get_current_user(
        session: str = Cookie(None),
        db: AsyncSession = Depends(get_db),
        session_storage=Depends(get_session_storage),
) -> User:
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session ID not provided"
        )

    user_id = await session_storage.get(session)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The session has expired. Please re-login"
        )

    return await User.by_id(db, int(user_id))
