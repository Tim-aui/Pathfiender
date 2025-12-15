from fastapi import APIRouter
from ..schemas import RegistrationUser, LoginUser
from services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from config.database import get_db
from helpers import *
from ..validators import auth_validators
from ..dependencies import get_services

router = APIRouter() 


@router.post("/registration")
async def registration(
    user: RegistrationUser,
    service: AuthService = Depends(get_services.get_auth_service),
    db: AsyncSession = Depends(get_db)
    ):
        return await service.create_user(user_payload=user, db=db)
        

@router.post("/login")
async def login(
    user: LoginUser = Depends(auth_validators.validate_auth_user),
    db: AsyncSession = Depends(get_db)
):  
    
    return await AuthService.create_tokens_for_user(user)
    