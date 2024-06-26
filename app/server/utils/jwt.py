from datetime import datetime, timedelta
from typing import Any
from bson import ObjectId


from dotenv import dotenv_values
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import exceptions, jwt
from server.database.database import db

config = dotenv_values(".env")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 90
ALGORITHM = "HS256"
JWT_SECRET_KEY = config["JWT_SECRET_KEY"]
JWT_REFRESH_SECRET_KEY = config["JWT_REFRESH_SECRET_KEY"]


async def create_access_token(subject: str | Any, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now() + expires_delta
    else:
        expires_delta = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta.timestamp(), "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def create_refresh_token(subject: str | Any, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now() + expires_delta
    else:
        expires_delta = datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta.timestamp(), "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def decode_jwt(token: str, secret_key: str = JWT_SECRET_KEY) -> dict | None:
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        expiration_time = datetime.fromtimestamp(decoded_token["exp"])
        return decoded_token if expiration_time >= datetime.now() else None
    except exceptions.JWTError as _:
        return None


async def refresh_access_token(refresh_token: str) -> str | None:
    decoded_token = decode_jwt(refresh_token, JWT_REFRESH_SECRET_KEY)
    if decoded_token is None:
        return None
    else:
        return create_access_token(decoded_token["sub"])


async def get_user(token: str) -> dict | None:
    decoded_token = await decode_jwt(token)
    return db.users.find_one({"_id": ObjectId(decoded_token["sub"])})


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not await self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            user = await get_user(credentials.credentials)
            return user
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    async def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid = await decode_jwt(jwt_token) is not None
        return is_token_valid
