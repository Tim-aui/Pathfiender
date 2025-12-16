from exceptions.error import DatabaseException 
from models import User
from utils.password import hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from fastapi import Depends


async def create_user(db: AsyncSession, user: User):
    with db.session.begin():
        db.session.add(user)
    return user
    