from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from models import User
from datetime import date
from utils.password import *
from utils import token
from api.v1.schemas import LoginUser, TokenInfo, RegistrationUser
from helpers import TOKEN_TYPE
from jwt.exceptions import InvalidTokenError
from uuid import uuid4
from services import user_service
import logger as logger_module_configurator 
from services.user_service import get_user_by_email
from exceptions.error import *


LOGGER_USER_SERVICE_NAME = "auth_service"

logger = logger_module_configurator.get_logger(LOGGER_USER_SERVICE_NAME)

async def create_user( 
        user_payload: RegistrationUser, 
        db: AsyncSession
        ):


    exist_user = await get_user_by_email(email=user_payload.email, db=db)

    if exist_user:
        raise UserAlreadyExistsException(user_payload.email)
    
    user = User(
        username=user_payload.username,
        active = True,
        email=user_payload.email, 
        password=hash_password(user_payload.password), 
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)
    
    logger.info(f"Пользователь создан: {user.id}, email: {user.email}")


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