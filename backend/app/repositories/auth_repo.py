from exceptions.error import DatabaseException 
from models import User
from utils.password import hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from fastapi import Depends


async def create_user(db: AsyncSession, user: User):

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user
    