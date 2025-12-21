from fastapi import HTTPException, status
from uuid import uuid4

class UserAlreadyExistsException(Exception):	
	def __init__(self):
		self.detail = "User is already registered"


class DatabaseException(Exception):
	def __init__(self, error_id: str):
		self.error_id = error_id
		self.detail = f"Interval server error. Please try again later.\n{self.error_id}"

class NotFoundException(Exception):
	def __init__(self):
		self.detail = "Ничего не найдено."
			

class NotPermissionException(Exception):
	def __init__(self):
		self.detail = "Недостаточно прав."
			
class TokenTypeInccorectException(Exception):
	def __init__(self):
		self.detail= f"Invalid token type"

class UnauthorizedException(Exception):
	def __init__(self):
		
		self.detail=f"Unauthorized user"
			
		
class InactiveUserException(Exception):
	def __init__(self):
		self.detail = f"Inactive User"


class PasswordValidationException(Exception):

	def __init__(self, problems: list):
		self.detail = problems