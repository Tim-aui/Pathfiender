from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from fastapi import Depends
from sqlalchemy import select
from models import User



async def get_user_by_email(
    email: str,
    db: AsyncSession,
):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def get_users(
    db: AsyncSession
):
    result = await db.execute(select(User))
    return result.scalars().all()
    
        
async def patch(
    db: AsyncSession,
    user: User
):
    
    await db.commit()
    await db.refresh(user)

async def delete(
    db: AsyncSession,
    user: User
):
    await db.delete(user)
    await db.commit()