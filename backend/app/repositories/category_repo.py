from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Category

async def get_all(db: AsyncSession):
    values = await db.execute(select(Category))

    return values.scalars().all()


async def create(db: AsyncSession, category: Category):
    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category


async def get_one_byId(db: AsyncSession, category_id: int):
    category = await db.execute(
        select(Category).where(Category.id == category_id)
    )

    return category.scalar_one_or_none()

async def delete(db: AsyncSession, category: Category):
    await db.delete(category)
    await db.commit()

async def patch(db: AsyncSession, category: Category):
    await db.commit()
    await db.refresh(category)