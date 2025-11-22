from fastapi import FastAPI
import uvicorn
from api.v1.routers.auth_router import router as auth_router
from api.v1.routers.user_router import router as user_router
from api.v1.routers.shop_router import router as shop_router
from api.v1.routers.product_router import router as product_router
from api.v1.routers.category_router import router as category_router
import os


app = FastAPI()

app.include_router(
    auth_router, 
    prefix=os.getenv("BASE_URL") + "/auth", 
    tags=["Auth"]
)
app.include_router(
    user_router,
    prefix=os.getenv("BASE_URL") + "/user",
    tags=["Users"]
)
app.include_router(
    shop_router,
    prefix=os.getenv("BASE_URL") + "/home",
    tags=["Shop"]
)
app.include_router(
    product_router,
    prefix=os.getenv("BASE_URL") + "/product",
    tags=["Products"]
)
app.include_router(
    category_router,
    prefix=os.getenv("BASE_URL") + "/category",
    tags=["Category"]
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)