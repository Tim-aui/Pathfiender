from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status, Depends
from models import User
from utils.password import *
from utils import token
from api.v1.schemas import LoginUser, TokenInfo, RegistrationUser
from helpers import TOKEN_TYPE
import logger as logger_module_configurator 
from exceptions.error import *
from repositories import user_repo, auth_repo
from config.database import get_db
from exceptions.handlers import databaseErrorHandler
from utils.password import passwordValidator

LOGGER_USER_SERVICE_NAME = "auth_service"

logger = logger_module_configurator.get_logger(LOGGER_USER_SERVICE_NAME)



async def create_user(
        user_payload: RegistrationUser, 
        db: AsyncSession
    ):


    
    
    exist_user = await user_repo.get_user_by_email(email=user_payload.email, db=db)

    if exist_user:
        logger.error(f"Пользователь с почтой {user_payload.email} уже создан")
        raise UserAlreadyExistsException()

    passwordValidator(user_payload.password)

    user = User(
                username=user_payload.username,
                active = True,
                email=user_payload.email, 
                password=hash_password(user_payload.password), 
            )

    try:
        new_user = await auth_repo.create_user(user=user, db=db)
        logger.info(f"Пользователь создан: {user.id}, email: {user.email}")
        
        return new_user

    except Exception as exc:
        await databaseErrorHandler(db=db, exc=exc, logger=logger)

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
    except Exception as exc:
        await databaseErrorHandler(exc=exc, logger=logger, rollback=False)