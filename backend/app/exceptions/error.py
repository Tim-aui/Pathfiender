from fastapi import HTTPException, status
from uuid import uuid4

class UserAlreadyExistsException(Exception):	
	detail = "User is already registered"


class DatabaseException(Exception):
	def __init__(self):
		super().__init__(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=
			{
				"detail": "Interval server error. Please try again later.",
				"error_id": uuid4()
			}
		)

class TokenTypeInccorectException(HTTPException):
	def __init__(self):
		super().__init__(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail={
				"detail": f"Invalid token type"
			}
		)

class UnauthorizedException(HTTPException):
	def __init__(self):
		super().__init__(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail={
				"detail": f"Unauthorized user"
			}
		)

class DefaultException(HTTPException):
	def __init__(self, error_id: str):
		super().__init__(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail={
				"detail": "Interval server error"
			},
			error_id = error_id

		)