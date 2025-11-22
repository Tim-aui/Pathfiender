from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from ..schemas import CategoryCreate

router = APIRouter()

@router.get("/categories")
async def categories(
    db: AsyncSession = Depends(get_db)
):
    pass

@router.post("/create")
async def create(
    category_payload: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    pass

@router.get("/{id}")
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    pass

@router.delete("/delete/{id}")
async def delete(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    pass

@router.patch("/{id}")
async def update(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    pass