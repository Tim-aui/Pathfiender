import uuid
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from logging import Logger
from exceptions import *


async def handle_database_error(
	db: AsyncSession,
	action: str,
	logger: Logger,
	context: Dict[str, None] = None,
	rollback: bool = True,
) -> DatabaseException:

	error_id = str(uuid.uuid4())
	context_str = " | ".join([f"{k}: {v}" for k, v in (context or {}).items()])

	logger.error(
		f"Error ID: {error_id} | "
		f"Action: {action} | "
		f"{context_str} | "
		f"Error type: DatabaseError",
		exc_info=True
	)

	if rollback:
		await db.rollback()

	return DatabaseException(error_id=error_id)

def handle_user_already_exists_error(
	email: str,
	logger: Logger
) -> UserAlreadyExistsException:
	
	logger.error(f"Попытка регистрации с существующей почтой {email}")

	return UserAlreadyExistsException(email=email)

def handle_token_type_inccorect_error(
	token_type: str,
	expected_token_type: str,
	logger: Logger,
) -> TokenTypeInccorectException:
	logger.error(
		f"Invalid token type received | "
        f"Expected: {expected_token_type} | "
        f"Received: {token_type}"
	)

	return TokenTypeInccorectException()


def handle_unauthorized_error(
	logger: Logger
) -> UnauthorizedException:
	pass


