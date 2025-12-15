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
from repositories.auth_repo import AuthRepository
from services.user_service import UserService

LOGGER_USER_SERVICE_NAME = "auth_service"

logger = logger_module_configurator.get_logger(LOGGER_USER_SERVICE_NAME)
class AuthService:

    def __init__(self):
        self.auth_repo = AuthRepository()
        self.user_service = UserService()

    async def create_user(
            self, 
            user_payload: RegistrationUser, 
            db: AsyncSession,
        ):


        exist_user = await self.user_service.get_user_by_email(email=user_payload.email, db=db)

        if exist_user:
            logger.error(f"Пользователь с почтой {user_payload.email} уже создан")
            raise UserAlreadyExistsException()

        user = User(
                    username=user_payload.username,
                    active = True,
                    email=user_payload.email, 
                    password=hash_password(user_payload.password), 
                )

        new_user = await self.auth_repo.create_user(user)
        
        logger.info(f"Пользователь создан: {user.id}, email: {user.email}")
        return new_user

    async def create_tokens_for_user(
        self,
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