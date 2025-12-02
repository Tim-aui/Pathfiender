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
from exceptions import UserAlreadyExistsException, DatabaseException
from error_handling import handle_database_error, handle_user_already_exists_error

LOGGER_USER_SERVICE_NAME = "auth_service"

logger = logger_module_configurator.get_logger(LOGGER_USER_SERVICE_NAME)

async def create_user(
        user_payload: RegistrationUser, 
        db: AsyncSession
        ):
    try:

        exist_user = await get_user_by_email(email=user_payload.email, db=db)

        if exist_user:
            raise handle_user_already_exists_error(email=user_payload.email, logger=logger)
        
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

        return user
    except HTTPException as e:
        raise
    except Exception as e:
        context = {
            "email": user_payload.email,
            "ErrorType": type(e).__name__
        }
        raise await handle_database_error(
            db=db,
            action="user:create",
            context=context,
            logger=logger,
            rollback=True
        )

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