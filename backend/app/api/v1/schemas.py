from pydantic import BaseModel


class RegistrationUser(BaseModel):
    username: str
    email: str
    password: str
    