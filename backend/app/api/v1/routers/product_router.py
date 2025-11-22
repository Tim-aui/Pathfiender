from fastapi import APIRouter, Depends
from ..schemas import ProductCreate, ProductUpdate
from services import product_service, user_service
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from models import User

router = APIRouter()

@router.get("/")
async def products(
    db: AsyncSession = Depends(get_db)
):
    return await product_service.get_all(db=db)

@router.post("/create")
async def create(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(user_service.get_current_auth_user)
):
    return await product_service.create_product(
        product_dict=product.dict(), 
        db=db, 
        user=current_user
    )

@router.get("/{id}")
async def product(id: str, db: AsyncSession = Depends(get_db)):
    return await product_service.get_one_product_by_id(id=id, db=db)

@router.patch("/update/{product_id}")
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: User = Depends(user_service.get_current_auth_user),
    db: AsyncSession = Depends(get_db)
):
    return await product_service.get_one_product_and_update(
        id=product_id, 
        patch_data=product_data,
        db=db,
        user=current_user
    )
    

@router.delete("/delete/{id}")
async def delete_product(
    product_id: int,
    current_user: User = Depends(user_service.get_current_auth_user),
    db: AsyncSession = Depends(get_db)
):
    return await product_service.get_one_and_drop(
        id=product_id, 
        db=db,
        user=current_user
    )
