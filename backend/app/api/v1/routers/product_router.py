from fastapi import APIRouter
from ..schemas import ProductCreate

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
async def create(product_payload: ProductCreate):
    return {"msg": product_payload}

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