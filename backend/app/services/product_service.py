from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.v1.schemas import ProductCreate, ProductUpdate
from fastapi import Depends, HTTPException, status
from models import User, Product
from uuid import uuid4
from datetime import date
from config.database import get_db



class ProductService:

	

	async def create_product(
		self,
		product_dict: dict,
		db: AsyncSession,
		user: User,
	) -> Product:
		try:
			

			product = Product(
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
			self,
			id: str,
			db: AsyncSession,
		):
			try:

				result = await db.execute(
					select(Product).where(Product.id == int(id))
				)

				product = result.scalar_one_or_none()

				if not product:
					raise HTTPException(
						status_code=status.HTTP_400_BAD_REQUEST,
						detail={"msg": "Incorrect input data"}
					)

				return product

			except Exception as e:
				raise HTTPException(
					status_code=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
					detail={"msg": f"Interval Server Error {e}"}
				)

	async def get_one_product_and_update(
			self,
			id: int,
			patch_data: ProductUpdate,
			user: User,
			db: AsyncSession
	):
		try:

			update_data = patch_data.dict(exclude_unset=True)

			product = await self.get_one_product_by_id(id=id, db=db)


			if user.id != product.creator_id:
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail={
						"msg": "Not permission"
					}
				)

			for field, value in update_data.items():
				if hasattr(product, field):
					if value != None:
						setattr(product, field, value)

			await db.commit()
			await db.refresh(product)
			
			return product

		except HTTPException:
			await db.rollback()
			raise
		except Exception as e:
			await db.rollback()
			print(f"Неожиданная ошибка: {str(e)}")
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				detail={
					"msg": "Внутренняя ошибка сервера"
				}
			)
		
	async def get_one_and_drop(
			self,
			id: int,
			user: User,
			db: AsyncSession = Depends(get_db)
	):
		try:
			
			product = await self.get_one_product_by_id(id=id, db=db)

			if user.id != product.creator_id:
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail={
						"msg": "Not permission"
					}
				)
			
			await db.delete(product)
			await db.commit()

			return {"msg": "Delete success"}

		except HTTPException:
			await db.rollback()
			raise
		except Exception as e:
			await db.rollback()
			print(f"Неожиданная ошибка: {str(e)}")
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				detail={
					"msg": "Внутренняя ошибка сервера"
				}
			)
		
	async def get_all(
			self,
			db: AsyncSession = Depends(get_db)
	):
		try:

			result = await db.execute(select(Product))

			product = result.scalars().all()

			return product

		except Exception as e:
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				detail={"msg": f"Interval Server Error {e}"}
			)