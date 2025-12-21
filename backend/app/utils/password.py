import bcrypt
import re
from exceptions.error import PasswordValidationException


def hash_password(password: str):
    salt = bcrypt.gensalt()
    bytes = password.encode("utf-8")
    hash = bcrypt.hashpw(bytes, salt)

    return hash.decode("utf-8")

def equal_passwords(input_password: str, exist_password: str):
    return bcrypt.checkpw(
        password=input_password.encode("utf-8"), 
        hashed_password=exist_password.encode("utf-8")
    )





def passwordValidator(password: str):
    problems = []

    if len(password) < 8:
        problems.append("минимальная длина пароля 8")
    
    if not re.search(r"A-Z", password):
        problems.append("пароль должен содержать заглавные буквы")
    if not re.search(r"a-z", password):
        problems.append("пароль должен содержать буквы")

    if not re.search(r"\d", password):
        problems.append("пароль долен содержать цифры")

    if not re.search(r"!-?", password):
        problems.append("пароль должен содержать спецсимволы") 

    if problems:
        raise PasswordValidationException(problems=problems)
    