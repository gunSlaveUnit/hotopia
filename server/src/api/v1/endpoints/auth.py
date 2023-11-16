import datetime
import uuid
from typing import Optional

from starlette import status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from core.models.users import User
from core.utils.auth import authenticate_user
from settings import AUTH_ROUTER_PREFIX, SESSION_TTL
from server.src.core.utils.crypt import get_password_hash
from api.v1.schemas.users import UserSignUpSchema, UserSignInSchema
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

    return await sign_in(
        UserSignInSchema(
            account_name=data.account_name,
            password=data.password
        ),
        db,
        session_storage
    )


@router.post('/sign-in/')
async def sign_in(
        data: UserSignInSchema,
        db: AsyncSession = Depends(get_db),
        session_storage=Depends(get_session_storage)
):
    user: Optional[User] = await authenticate_user(db, data.account_name, data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect account name or password"
        )

    session_id = str(uuid.uuid4())
    await session_storage.set(session_id, user.id)
    await session_storage.expire(session_id, SESSION_TTL)

    response = JSONResponse({"detail": "Logged in successfully"})
    response.set_cookie("session", session_id, max_age=SESSION_TTL)

    await user.update(db, {"login_at": datetime.datetime.now()})

    return response
