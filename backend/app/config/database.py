from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

# Создаем сессию
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Функция для получения сессии
async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()