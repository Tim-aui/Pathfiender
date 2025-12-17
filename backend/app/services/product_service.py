from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.v1.schemas import ProductCreate, ProductUpdate
from fastapi import Depends, HTTPException, status
from models import User, Product
from uuid import uuid4
from datetime import date
from config.database import get_db
from repositories import product_repo
import logger as logger_module_configurator
from exceptions.handlers import databaseErrorHandler
from exceptions.error import *

logger = logger_module_configurator.get_logger("product_service")


async def create_product(
	product_dict: dict,
	db: AsyncSession,
	user: User,
) -> Product:


	

	product = Product(
		title = product_dict["title"],
		description = product_dict["description"],
		creator_id = user.id,
		create_at = date.today()
	)

	try:
		
		product = await product_repo.create(db=db, product=product)

		logger.info(f"Товар успешно создан {product.id}")

		return product

	except Exception as exc:
		await databaseErrorHandler(db=db, exc=exc, logger=logger)

		
async def get_one_product_by_id(
		product_id: int,
		db: AsyncSession,
	):
	
	product = await product_repo.get_one_byId(db=db, product_id=product_id)

	if not product:
		logger.error(f"Не удалось найти товар {product_id}")
		raise NotFoundException()

	return product


async def get_one_product_and_update(
		product_id: int,
		patch_data: ProductUpdate,
		user: User,
		db: AsyncSession
):


	update_data = patch_data.dict(exclude_unset=True)

	product = await product_repo.get_one_byId(product_id=product_id, db=db)


	if user.id != product.creator_id:
		raise NotPermissionException()

	for field, value in update_data.items():
		if hasattr(product, field):
			if value != None:
				setattr(product, field, value)

	try:
		await product_repo.patch(db=db, product=product)
		logger.info(f"Товар {product.id} успешно обновлен")
		return product

	except Exception as exc:
		await databaseErrorHandler(exc=exc, logger=logger, db=db, rollback=False)
	
async def get_one_and_drop(
		product_id: int,
		user: User,
		db: AsyncSession = Depends(get_db)
):
	
	
	product = await get_one_product_by_id(product_id=product_id, db=db)

	if user.id != product.creator_id:
		raise NotPermissionException()
	
	try:

		await product_repo.delete(db=db, product=product)
		logger.info(f"Товар {product.id} успешно удален")
		return {"msg": "Delete success"}

	except Exception as exc:
		await databaseErrorHandler(exc=exc, logger=logger, db=db, rollback=False)

	

	
	
async def get_all(
		db: AsyncSession = Depends(get_db)
):
	try:

		products = await product_repo.get_all(db=db)

		return products

	except Exception as exc:
		await databaseErrorHandler(exc=exc, logger=logger, db=db, rollback=False)