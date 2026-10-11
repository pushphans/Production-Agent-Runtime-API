from uuid import UUID
from fastapi import status
from fastapi.responses import JSONResponse
from production_agent_runtime_api.models.user_model import UserModel
from sqlalchemy import select
from production_agent_runtime_api.core.db import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, datetime, timezone
from production_agent_runtime_api.core.config import settings
import jwt
from pwdlib import PasswordHash
import secrets
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



password_hasher = PasswordHash.recommended()

security = HTTPBearer()



def hash_password(password : str) -> str:
    return password_hasher.hash(password=password)


def verify_password(hash_password, password) -> bool:
    return password_hasher.verify(password=password, hash=hash_password)



def create_access_token(user_id : UUID) -> str:
    payload = {
        "sub" : str(user_id),
        "exp" : datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_IN_MINUTES)
    }

    token = jwt.encode(
        algorithm=settings.ALGORITHM,
        payload=payload,
        key=settings.JWT_SECRET_KEY
    )

    return token



def decode_jwt(token : str):
    decoded_token = jwt.decode(
        token,
        algorithms=[settings.ALGORITHM],
        key=settings.JWT_SECRET_KEY,
    )

    return decoded_token


def create_refresh_token():
    return secrets.token_urlsafe(64)


async def get_user(
    db : AsyncSession = Depends(get_db),
    credentials : HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = decode_jwt(token=token)

    user_id = payload.get("sub")

    user_exists_check_query = (
        select(UserModel)
        .where(UserModel.id == user_id)
    )

    user_exists_result = await db.execute(user_exists_check_query)

    user_exists = user_exists_result.scalar_one_or_none()

    if user_exists is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail" : "Invalid token"}
        )

    return user_exists
