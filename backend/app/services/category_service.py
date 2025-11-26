from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Category, User
from fastapi import HTTPException, status, Depends
from api.v1.schemas import CategoryCreate, CategoryUpdate
from datetime import date
from slugify import slugify

async def get_categories(
    db: AsyncSession
):
    try:
        result = await db.execute(select(Category))

        return result.scalars().all()

    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"detail": f"Server Error {e}"}
        )
    
async def create_category(
    category_dict: dict,
    user: User,
    db: AsyncSession,
):  
    try:

        slug = slugify(category_dict["title"])

        category = Category(
            title = category_dict["title"],
            description = category_dict["description"],
            slug = slug,
            creator_id = user.id
        )

        db.add(category)
        await db.commit()
        await db.refresh(category)

        return category

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"detail": f"Server Error {e}"}
        )
    
async def get_one_category_by_id(
    category_id: int,
    db: AsyncSession,
):
    try:
        category = await db.execute(select(Category).where(Category.id == category_id))

        result = category.scalar_one_or_none()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"detail": "Category does not exist"}
            )

        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"detail": f"Interval Server Error {e}"}
        )
    
async def get_one_and_drop(
        category_id: int,
        user: User,
        db: AsyncSession,
):
    try:

        category = await get_one_category_by_id(category_id=category_id, db=db)

        if category.creator_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"detail": "Not Rules"}
            )

        await db.delete(category)
        await db.commit()   

        return {"msg": "Category delete success"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"detail": f"Server Interval Error {e}"}
        ) 
    
async def get_one_and_patch(
        category_id: int,
        patch_data: CategoryUpdate,
        user: User,
        db: AsyncSession
):
    
    try:
        
        category = await get_one_category_by_id(
            category_id=category_id,
            db=db
        )

        if category.creator_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"detail": "Not Rules"}
            )

        update_data = patch_data.dict(exclude_unset=True)

        if "title" in update_data and update_data["title"] != category.title:
            update_data["slug"] = slugify(update_data["title"])


        for field, value in update_data.items():
            if hasattr(category, field):
                if value != None:
                    setattr(category, field, value)

        await db.commit()
        await db.refresh(category)
		
        return category


    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"detail": f"Interval Server Error {e}"}
        )