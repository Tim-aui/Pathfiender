import re
from ....exceptions.error import PasswordValidationException


def passwordValidator(password: str):
    problems = []

    if len(password) < 8:
        problems += "минимальная длина пароля 8"
    
    if not re.search(r"A-Z", password):
        problems += "пароль должен содержать заглавные буквы"
    if not re.search(r"a-z", password):
        problems += "пароль должен содержать буквы"

    if not re.search(r"\d", password):
        problems += "пароль долен содержать цифры"

    if not re.search(r"!-?", password):
        problems += "пароль должен содержать спецсимволы"

    if problems:
        raise PasswordValidationException(problems=problems)
    