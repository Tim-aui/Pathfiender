from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from models import Users
from datetime import date

async def get_users(
        db: AsyncSession
):
    try:
        result = await db.execute(select(Users))

        return result.scalar_one_or_none()
    
    except Exception as e:
        await db.rollback()
        raise HTTPException("505", f"Server error {e}")

async def create_user(
        user_dict: dict, 
        db: AsyncSession
        ):
    try:
        user = Users(
            id=3,
            username=user_dict["username"], 
            email=user_dict["email"], 
            password=user_dict["password"], 
            role=["Gondon"], 
            create_at=date.today()
        )

        db.add(user)

        await db.commit()
        await db.refresh(user)

        return user
    except Exception as e:
        await db.rollback()
        raise HTTPException("505", f"Server error {e}")