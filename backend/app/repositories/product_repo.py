from sqlalchemy.ext.asyncio import AsyncSession
from models import Product
from sqlalchemy import select

async def get_all(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()

async def create(db: AsyncSession, product: Product):
    db.add(product)
    await db.commit()
    await db.refresh(product)

    return product

async def get_one_byId(db: AsyncSession, product_id: int):
    result = await db.execute(
		select(Product).where(Product.id == product_id)
	)

    return result.scalar_one_or_none()

async def delete(db: AsyncSession, product: Product):
    await db.delete(product)
    await db.commit()

async def patch(db: AsyncSession, product: Product):
    await db.commit()
    await db.refresh(product)