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

logger = logger_module_configurator.get_logger('auth_service')
async def create_user(
        user_payload: RegistrationUser, 
        db: AsyncSession
        ):
    try:

        exist_user = await get_user_by_email(email=user_payload.email, db=db)

        if exist_user:
            logger.error(f"Попытка регистрации с существующей почтой {user_payload.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"detail": "User is already registered"}
            )

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
        error_id = str(uuid4())

        logger.error(
            f"Error ID: {error_id} | "
            f"Email: {user_payload.email} | "
            f"Action: create_product | "
            f"Error type: {type(e).__name__}",
            exc_info=True
        )

        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={
                "msg": "Internal server error. Please try again later.",
                "error_id": error_id
            }
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