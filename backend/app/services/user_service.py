from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, Depends, status
from api.v1.schemas import TokenInfo, UpdateUser
from models import Users
from utils.token import get_current_token_payload
from config.database import get_db
import os
from helpers import *
from utils.token import *
from typing import Annotated

async def get_user_by_email(
    email: str,
    db: AsyncSession      
):
    try:

        result = await db.execute(
            select(Users).where(Users.email == email)
        )

        return result.scalar_one_or_none()

    except Exception as e:
        await db.rollback()
        raise HTTPException("505", f"Server error {e}")
    
async def get_users(
        db: AsyncSession
):
    try:
        result = await db.execute(select(Users))

        return result.scalars().all()
    
    except Exception as e:
        raise HTTPException("505", f"Server error {e}")

async def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
        db: AsyncSession = Depends(get_db)
) -> Users:  
    token_type = payload.get(TOKEN_TYPE_FIELD)

    if token_type != ACCESS_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'invalid token type {token_type!r} excepted {ACCESS_TOKEN_TYPE!r}'
        )
    
    email: str | None = payload.get("sub")
    user = await get_user_by_email(email, db)

    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)"
    )


async def get_current_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
    db: AsyncSession = Depends(get_db)
): 
    token_type = payload.get(TOKEN_TYPE_FIELD)

    if token_type != REFRESH_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'invalid token type {token_type!r} excepted {REFRESH_TOKEN_TYPE!r}'
        )
    
    email: str | None = payload.get("sub")
    user = await get_user_by_email(email, db)

    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)"
    )


def auth_user_check_self_info(
    user: Users = Depends(get_current_auth_user)    
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="inactive user"
    )

def refresh_tokens(
    current_user: dict = Depends(get_current_user_for_refresh),
):  
    try:
        
        access_token = create_access_token(current_user)
        refresh_token = create_refresh_token(current_user)

        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=TOKEN_TYPE
        )
    except InvalidTokenError:
        raise HTTPException(
        status_code=401,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_user_and_update(
        patch_data: UpdateUser, 
        user: Users = Depends(get_current_auth_user),
        db: AsyncSession = Depends(get_db)
):  
    try:
        update_data = patch_data.dict(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(user, field):
                if value != None:
                    setattr(user, field, value)

        await db.commit()
        await db.refresh(user)

        return user

    except Exception as e:
        await db.rollback() 
        raise HTTPException(
            status_code=500, 
            detail=f"Ошибка обновления: {str(e)}"
        )
    
async def get_user_and_delete(
    db: AsyncSession = Depends(get_db),
    user: Users = Depends(get_current_auth_user)
):
    
    try:
        await db.delete(user)
        await db.commit()

        return {"msg": "User deleted"}

    except Exception as e:
        await db.rollback() 
        raise HTTPException(
            status_code=500, 
            detail=f"Ошибка при удаления: {str(e)}"
        )

