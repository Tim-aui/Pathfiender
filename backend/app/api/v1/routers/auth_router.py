from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas import RegistrationUser, LoginUser, TokenInfo
from services import auth_service, user_service
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from config.database import get_db
from utils import token
from helpers import *
from ..validators import auth_validators

router = APIRouter()

@router.get("/getter")
async def getter(
    db: AsyncSession = Depends(get_db)
):  
    return await user_service.get_users(db)
    

@router.post("/registration")
async def registration(
    user: RegistrationUser,
    db: AsyncSession = Depends(get_db)
    ):
        return await auth_service.create_user(user_dict=user.dict(), db=db)
        

@router.post("/login")
async def login(
    user: LoginUser = Depends(auth_validators.validate_auth_user),
    db: AsyncSession = Depends(get_db)
):  
    
    return await auth_service.create_tokens_for_user(user)
    