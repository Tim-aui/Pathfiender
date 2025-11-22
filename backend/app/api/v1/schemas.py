from typing import Optional
from pydantic import BaseModel
from datetime import date

class RegistrationUser(BaseModel):
    username: str
    email: str
    password: str

class LoginUser(BaseModel):
    email: str
    password: str


class UpdateUser(BaseModel):
    username: Optional[str] | None = None
    email: Optional[str] | None = None
    password: Optional[str] | None = None
    role: Optional[list[str]] | None = None



class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str




class ProductCreate(BaseModel):
    title: str
    description: str
    category_id: str

class ProductUpdate(BaseModel):
    title: str
    description: str

class CategoryCreate(BaseModel):
    name: str
    description: str
