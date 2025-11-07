from fastapi import APIRouter
from ..schemas import RegistrationUser
from services import auth_service
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from config.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/getter")
async def getter(
    db: AsyncSession = Depends(get_db)
):
    return await auth_service.get_users(db)

@router.post("/registration")
async def registration(
    user: RegistrationUser,
    db: AsyncSession = Depends(get_db)
    ):
    user = await auth_service.create_user(user_dict=user.dict(), db=db)

    return user