from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from models import Users
from datetime import date
from utils.password import *
from utils import token
from api.v1.schemas import LoginUser, TokenInfo
from helpers import TOKEN_TYPE
from jwt.exceptions import InvalidTokenError
from uuid import uuid4
from services import user_service

async def create_user(
        user_dict: dict, 
        db: AsyncSession
        ):
    try:
        user = Users(
            id=len(await user_service.get_users(db)) + 1,
            username=user_dict["username"], 
            active = True,
            email=user_dict["email"], 
            password=hash_password(user_dict["password"]), 
            role=["user"], 
            create_at=date.today()
        )

        db.add(user)

        await db.commit()
        await db.refresh(user)

        return user
    except Exception as e:
        await db.rollback()
        raise HTTPException(500, f"Server error {e}")

async def create_tokens_for_user(
    user: LoginUser
):
    try:
        access_token = token.create_access_token(user=user)
        refresh_token = token.create_refresh_token(user=user)

        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=TOKEN_TYPE
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
            detail=f"Server error {e}"
        )