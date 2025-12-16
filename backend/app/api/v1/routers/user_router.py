from fastapi import APIRouter, Depends, HTTPException
from ..schemas import TokenInfo, UpdateUser
from config.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from services import user_service

router = APIRouter()


@router.get("/whoami")
async def whoami(
    user: User = Depends(user_service.auth_user_check_self_info)
):
    return user 
@router.get("/refresh")
async def refresh(tokens: TokenInfo = Depends(user_service.refresh_tokens)):
    return tokens   
    
@router.patch("/update")
async def update(
    updated_user: User = Depends(user_service.get_user_and_update)
):
    return updated_user

@router.delete("/delete")
async def delete(
    result: dict = Depends(user_service.get_user_and_delete)
):
    return result
     