from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.v1.schemas import ProductCreate
from fastapi import Depends, HTTPException, status
from models import Users, Products
from services import user_service
from uuid import uuid4
from datetime import date
from config.database import get_db

async def create_product(
	product_dict: dict,
	db: AsyncSession,
	user: Users,
) -> Products:
	try:
		

		product = Products(
			id = str(uuid4()),
			title = product_dict["title"],
			description = product_dict["description"],
			creator_id = user.id,
			create_at = date.today()
		)

		db.add(product)
		
		await db.commit()
		await db.refresh(product)

		return product
	
	except Exception as e:
		await db.rollback()
		raise HTTPException(
			status_code= status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
			detail={"msg": f"Server Interval error {e}"} 
		)
async def get_one_product_by_id(
		id: str,
		db: AsyncSession,
	):
		try:

			product = await db.execute(select(Products).where(Products.id == id))

			if not product:
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail={"msg": "Incorrect input data"}
				)

			return product

		except Exception as e:
			raise HTTPException(
				status_code=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
				detail={"msg": "Interval Server Error {e}"}
			)