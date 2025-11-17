import os
import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from datetime import timedelta, datetime
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from api.v1.schemas import LoginUser, User
from config.security import http_bearer
from fastapi import status

load_dotenv()

from helpers import *


def encode_jwt(
        payload: dict,
        private_key: str = os.getenv("SECRET_KEY"),
        algorithm: str = os.getenv("ALGORITHM"),
        expires_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")),
        expires_timedelta: timedelta | None = None
):
    to_encode = payload.copy()
    now = datetime.utcnow()

    if expires_timedelta:
        expire = now + expires_timedelta
    else:
        expire = now + timedelta(minutes=expires_minutes)

    to_encode.update(
        exp = expire,
        iat = now,
    )

    return jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm
    )

def decode_jwt(
        token: str | bytes,
        public_key: str = os.getenv("SECRET_KEY"),
        algorithm: str = os.getenv("ALGORITHM")
) -> dict:
    
    return jwt.decode(
        token,
        public_key,
        algorithms=algorithm
    )

def create_jwt(
        token_data: dict,
        token_type: str,
        expires_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")), expires_timedelta: timedelta | None = None
):
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)

    return encode_jwt(
        payload=jwt_payload,
        expires_minutes=expires_minutes,
        expires_timedelta=expires_timedelta
    )

def create_access_token(
        user: User
) -> str:
    jwt_payload = {
        "sub": user.email,
        "username": user.username,
        "email": user.email
    }

    return create_jwt(
        token_data=jwt_payload,
        token_type=ACCESS_TOKEN_TYPE,
        expires_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )

def create_refresh_token(
    user: LoginUser      
):
    jwt_payload = {
        "sub": user.email
    }

    return create_jwt(
        token_data=jwt_payload,
        token_type=REFRESH_TOKEN_TYPE,
        expires_timedelta=timedelta(
            days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
        )
    )

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    try:
        token = credentials.credentials

        return jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")],
            options={"verify_exp": True}
        )
        
    except InvalidTokenError:
        raise HTTPException(
        status_code=401,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
security = HTTPBearer()

async def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    
    try:
        payload = decode_jwt(
            token=credentials.credentials
        )

        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}"
        )
    
