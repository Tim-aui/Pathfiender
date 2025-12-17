from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Category, User
from fastapi import HTTPException, status, Depends
from api.v1.schemas import CategoryCreate, CategoryUpdate
from datetime import date
import logger as logger_module_configurator
from repositories import category_repo
from exceptions.error import *
from uuid import uuid4
from slugify import slugify
from exceptions.handlers import databaseErrorHandler

logger = logger_module_configurator.get_logger("category_service")

async def get_categories(
    db: AsyncSession
):
    try:
        result = await category_repo.get_all(db=db)

        return result

    except Exception as exc:
        await databaseErrorHandler(db=db, exc=exc, logger=logger, rollback=False)
    
async def create_category(
    category_dict: dict,
    user: User,
    db: AsyncSession,
):  
   

    slug = slugify(category_dict["title"])

    category = Category(
        title = category_dict["title"],
        description = category_dict["description"],
        slug = slug,
        creator_id = user.id
    )

    try:
        
        category = await category_repo.create(db=db, category=category)

        logger.info(f"Категория успешно создана: {category.id} | {category.title}")

        return category

    except Exception as exc:
        await databaseErrorHandler(db=db, exc=exc, logger=logger)
    
async def get_one_category_by_id(
    category_id: int,
    db: AsyncSession,
):
    try:
        category = await category_repo.get_one_byId(
            db=db, 
            category_id=category_id
        )
        if not category:
            raise NotFoundException()

        return category
    
    except Exception as exc:
        await databaseErrorHandler(db=db, exc=exc, logger=logger, rollback=False)
    
async def get_one_and_drop(
        category_id: int,
        user: User,
        db: AsyncSession,
):
    try:

        category = await category_repo.get_one_byId(category_id=category_id, db=db)

        if category.creator_id != user.id:
            raise NotPermissionException()

        await category_repo.delete(db=db, category=category)
        logger.info(f"Категория {category.id}, успешно удалена")

        return {"msg": "Category delete success"}

    except Exception as exc:
        await databaseErrorHandler(db=db, exc=exc, logger=logger)
    
async def get_one_and_patch(
        category_id: int,
        patch_data: CategoryUpdate,
        user: User,
        db: AsyncSession
):

    
    category = await category_repo.get_one_byId(
        category_id=category_id,
        db=db
    )

    if category.creator_id != user.id:
        raise NotPermissionException()

    update_data = patch_data.dict(exclude_unset=True)

    if "title" in update_data:
        update_data["slug"] = slugify(update_data["title"])


    for field, value in update_data.items():
        if hasattr(category, field):
            if value != None:
                setattr(category, field, value)

    try:

        await category_repo.patch(db=db, category=category)

        logger.info(f"Категория {category.id} успешно обновлена")

        return category
    
    except Exception as exc:
        await databaseErrorHandler(db=db, exc=exc, logger=logger)
    

    