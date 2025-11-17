from fastapi.responses import RedirectResponse
from ..schemas import LoginUser
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from config.database import get_db
from services import user_service
import os
from utils.password import *

async def validate_auth_user(
    user: LoginUser,
    db: AsyncSession = Depends(get_db)
):
    try:
        exist_user = await user_service.get_user_by_email(user.email, db)

        if not exist_user:
            return RedirectResponse(os.getenv("BASE_URL") + "/auth/registration")

        if equal_passwords(user.password, exist_user.password):
            return exist_user
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="incorrect user"
            )
    except Exception as e:
        raise e