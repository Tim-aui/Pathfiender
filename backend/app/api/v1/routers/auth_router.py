from fastapi import APIRouter
from ..schemas import RegistrationUser, LoginUser
from fastapi import Depends
from helpers import *
from ..validators import auth_validators
from services import auth_service
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db

router = APIRouter() 

@router.post("/registration")
async def registration(
    user: RegistrationUser,
    db: AsyncSession = Depends(get_db)
    ):
        return await auth_service.create_user(user_payload=user, db=db)
        

@router.post("/login")
async def login(
    user: LoginUser = Depends(auth_validators.validate_auth_user),
):  
    
    return await auth_service.create_tokens_for_user(user)
    