from config.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth_service import AuthService
from services.category_service import CategoryService
from services.product_service import ProductService
from services.user_service import UserService


def get_auth_service(db: AsyncSession = Depends(get_db)):
    return AuthService(db=db)

def get_category_service():
    return CategoryService()

def get_product_service():
    return ProductService()

def get_user_service():
    return UserService()