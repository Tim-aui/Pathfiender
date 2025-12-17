from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, Depends, status
from api.v1.schemas import TokenInfo, UpdateUser
from models import User
from utils.token import get_current_token_payload
from config.database import get_db
import os
from helpers import *
from utils.token import *
from typing import Annotated
import logger as logger_module_configurator
from repositories import user_repo
from exceptions.handlers import databaseErrorHandler
from exceptions.error import *
import logger as logger_module_configurator

logger = logger_module_configurator.get_logger("user_service")

async def get_user_by_email(
    email: str,
    db: AsyncSession
):
    try:

        return await user_repo.get_user_by_email(email=email, db=db)

    except Exception as exc:
        await databaseErrorHandler(exc=exc, logger=logger, db=db, rollback=False)

async def get_users(
        db: AsyncSession
):
    try:
        return await user_repo.get_users(db=db)
    
    except Exception as exc:
        await databaseErrorHandler(exc=exc, logger=logger, db=db, rollback=False)

async def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
        db: AsyncSession = Depends(get_db)
) -> User:  
    token_type = payload.get(TOKEN_TYPE_FIELD)

    if token_type != ACCESS_TOKEN_TYPE:
        logger.error(f"ожидался {ACCESS_TOKEN_TYPE} передан {REFRESH_TOKEN_TYPE}")
        raise TokenTypeInccorectException()
    
    email: str | None = payload.get("sub")
    user = await user_repo.get_user_by_email(email=email, db=db)

    if user:
        return user
    
    raise UnauthorizedException()


async def get_current_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
    db: AsyncSession = Depends(get_db)
): 
    token_type = payload.get(TOKEN_TYPE_FIELD)

    if token_type != REFRESH_TOKEN_TYPE:
        logger.error(f"Ожидался {REFRESH_TOKEN_TYPE} передан {ACCESS_TOKEN_TYPE}")
        raise TokenTypeInccorectException()
    
    email: str | None = payload.get("sub")
    user = await user_repo.get_user_by_email(email, db)

    if user:
        return user
    raise NotFoundException()


def auth_user_check_self_info(
    user: User = Depends(get_current_auth_user)    
):
    if user.active:
        return user
    raise InactiveUserException()

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
        user: User = Depends(get_current_auth_user),
        db: AsyncSession = Depends(get_db)
):  
    
    update_data = patch_data.dict(exclude_unset=True)

    for field, value in update_data.items():
        if hasattr(user, field):
            if value != None:
                setattr(user, field, value)

    try:
        
        await user_repo.patch(db=db, user=user)
        return user

    except Exception as exc:
        await databaseErrorHandler(exc=exc, logger=logger, db=db)
    
async def get_user_and_delete(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_auth_user)
):
    
    try:
        await user_repo.delete(db=db, user=user)
        logger.info(f"Пользователь {user.id} успешно удален")
        return {"msg": "User deleted"}

    except Exception as exc:
        await databaseErrorHandler(exc=exc, logger=logger, db=db)

