from starlette import status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from core.models.users import User
from settings import AUTH_ROUTER_PREFIX
from core.utils.crypt import get_password_hash
from api.v1.schemas.users import UserSignUpSchema
from core.utils.db import get_db, get_session_storage

router = APIRouter(prefix=AUTH_ROUTER_PREFIX)


@router.post('/sign-up')
async def sign_up(
        data: UserSignUpSchema,
        db: AsyncSession = Depends(get_db),
        session_storage=Depends(get_session_storage)
):
    same_email_user = await User.by_email(db, data.email)
    same_account_name_user = await User.by_account_name(db, data.account_name)

    if same_email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the same email address already exists"
        )

    if same_account_name_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the same account name already exists"
        )

    user = User(
        email=data.email,
        account_name=data.account_name,
        displayed_name=f'User #{select(func.count(User.id))}',
        password=get_password_hash(data.password),
        is_active=True,
    )

    _ = await User.create(db, user)