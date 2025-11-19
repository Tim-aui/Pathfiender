from fastapi import APIRouter, Depends
from ..schemas import ProductCreate
from services import product_service, user_service
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from models import Users

router = APIRouter()

@router.get("/")
async def products():
    return {
        "products": [
            "awdawd",
            "abfdbd",
            "jytrrt",
            "0-db-f"
        ]
    }

@router.post("/create")
async def create(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(user_service.get_current_auth_user)
):
    return await product_service.create_product(
        product_dict=product.dict(), 
        db=db, 
        user=current_user
    )

@router.get("/{id}")
async def product(id: str, db: AsyncSession = Depends(get_db)):
    return await product_service.get_one_product_by_id(id=id, db=db)

@router.patch("/update/{id}")
async def update_product(product_id: str):
    
    return {
        "msg": product_id
    }

@router.delete("/delete/{id}")
async def delete_product(product_id: str):
    return {
        "msg": product_id
    }