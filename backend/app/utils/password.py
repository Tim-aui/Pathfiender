import bcrypt

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
