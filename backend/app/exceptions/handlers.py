from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from exceptions.error import DatabaseException
from logging import Logger

async def databaseErrorHandler(
        exc: Exception, 
        logger: Logger,
        db: AsyncSession | None = None, 
        rollback: bool = True
):
    if rollback:
        await db.rollback()
    error_id = str(uuid4())
    logger.error(f"При создании пользователя произошла ошибка | "
                f"ID ошибки - {error_id} | "
                f"Error - {exc} | "
    )
    raise DatabaseException(error_id)