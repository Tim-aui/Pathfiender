from exceptions.error import DatabaseException 
from models import User
from utils.password import hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from fastapi import Depends
class AuthRepository:
    def __init__(self):
        self.db = Depends(get_db)


    async def create_user(self, user: User):
        with self.db.session.begin():
            self.db.session.add(user)
        return user
        