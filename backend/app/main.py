from fastapi import FastAPI, HTTPException
import logger as logger_module_configurator 
import uvicorn
from api.v1.routers.auth_router import router as auth_router
from api.v1.routers.user_router import router as user_router
from api.v1.routers.shop_router import router as shop_router
from api.v1.routers.product_router import router as product_router
from api.v1.routers.category_router import router as category_router
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder
from exceptions.error import UserAlreadyExistsException
from exceptions.factory import *

logger = logger_module_configurator.get_logger('main')

app = FastAPI()

app.include_router(
    auth_router, 
    prefix=os.getenv("BASE_URL") + "/auth", 
    tags=["Auth"]
)
logger.info("Auth Router Include")
app.include_router(
    user_router,
    prefix=os.getenv("BASE_URL") + "/user",
    tags=["Users"]
)
logger.info("User Router Include")
app.include_router(
    shop_router,
    prefix=os.getenv("BASE_URL") + "/home",
    tags=["Shop"]
)
logger.info("Shop Router Include")
app.include_router(
    product_router,
    prefix=os.getenv("BASE_URL") + "/product",
    tags=["Products"]
)
logger.info("Products Router Include")
app.include_router(
    category_router,
    prefix=os.getenv("BASE_URL") + "/category",
    tags=["Category"]
)
logger.info("Category Router Include")

origins = ["*"]



app.add_exception_handler(UserAlreadyExistsException, ExceptionResponseFactory(401))


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)