import datetime
import uuid
from typing import Optional

from starlette import status
from sqlalchemy import select, func
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Cookie

from server.src.core.models.users import User
from server.src.core.settings import SESSION_TTL
from server.src.core.utils.crypt import get_password_hash
from server.src.core.utils.db import get_db, get_session_storage
from server.src.core.utils.auth import authenticate_user, get_current_user
from common.src.api.v1.schemas.users import UserSignUpSchema, UserSignInSchema
from server.src.core.settings import AUTH_ROUTER_PREFIX, SIGN_UP_URL, SIGN_IN_URL, SIGN_OUT_URL, ME_URL

router = APIRouter(prefix=AUTH_ROUTER_PREFIX)


@router.post(SIGN_UP_URL)
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

    user_number_displayed_name = await db.scalar(select(func.count(User.id)))

    user = User(
        email=data.email,
        account_name=data.account_name,
        displayed_name=f'User #{user_number_displayed_name}',
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


@router.post(SIGN_IN_URL)
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


@router.post(SIGN_OUT_URL)
async def sign_out(
        session: str = Cookie(),
        session_storage=Depends(get_session_storage),
) -> JSONResponse:
    """Deletes a user session."""

    if session in session_storage:
        session_storage.delete(session)

        response = JSONResponse({"detail": f"Session {session} was removed"})
        response.delete_cookie('session')

        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session} not found"
        )


@router.get(ME_URL)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
