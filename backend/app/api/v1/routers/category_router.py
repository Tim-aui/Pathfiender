from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from ..schemas import CategoryCreate, CategoryUpdate
from services import category_service, user_service
from models import User
from services.user_service import UserService



router = APIRouter()
user_service = UserService()

@router.get("/categories")
async def categories(
    db: AsyncSession = Depends(get_db)
):
    return await category_service.get_categories(db)

@router.post("/create")
async def create(
    category_payload: CategoryCreate,
    user: User = Depends(user_service.get_current_auth_user),
    db: AsyncSession = Depends(get_db)
):
    return await category_service.create_category(
        category_dict=category_payload.dict(),
        user=user,
        db=db
    )
@router.get("/{id}")
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await category_service.get_one_category_by_id(
        category_id=category_id, 
        db=db
    )

@router.delete("/delete/{id}")
async def delete(
    category_id: int,
    user: User = Depends(user_service.get_current_auth_user),
    db: AsyncSession = Depends(get_db),

):
    return await category_service.get_one_and_drop(
        category_id=category_id,
        user=user,
        db=db
    )

@router.patch("/{id}")
async def update(
    category_id: int,
    category_patch: CategoryUpdate,
    user: User = Depends(user_service.get_current_auth_user),
    db: AsyncSession = Depends(get_db)
):
    return await category_service.get_one_and_patch(
        category_id=category_id, 
        patch_data=category_patch, 
        user=user,
        db=db
    )