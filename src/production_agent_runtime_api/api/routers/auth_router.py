from production_agent_runtime_api.schemas.auth_schemas import RefreshTokenResponseSchema
from production_agent_runtime_api.schemas.auth_schemas import RefreshTokenRequestSchema
from production_agent_runtime_api.core.security import get_user
from datetime import timedelta, timezone, datetime
from production_agent_runtime_api.schemas.auth_schemas import LoginResponseSchema
from production_agent_runtime_api.core.security import create_refresh_token
from production_agent_runtime_api.models.refresh_token import RefreshTokenModel
from production_agent_runtime_api.core.config import settings
from production_agent_runtime_api.core.security import create_access_token
from production_agent_runtime_api.core.security import verify_password
from production_agent_runtime_api.schemas.auth_schemas import LoginRequestSchema
from uuid import UUID
from production_agent_runtime_api.schemas.auth_schemas import RegisterResponseSchema
from production_agent_runtime_api.core.security import hash_password
import uuid
from fastapi import status
from fastapi import HTTPException
from production_agent_runtime_api.models.user_model import UserModel
from sqlalchemy import select
from production_agent_runtime_api.core.db import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from production_agent_runtime_api.schemas.auth_schemas import RegisterRequestSchema
from fastapi import APIRouter


auth_router = APIRouter(prefix="/auth", tags=["AUTH"])


@auth_router.post("/register")
async def register_user(data : RegisterRequestSchema, db : AsyncSession = Depends(get_db)):
    check_query = (
        select(UserModel)
        .where(UserModel.email == data.email)
    )

    user_already_exists_result = await db.execute(check_query)

    user_already_exists = user_already_exists_result.scalar_one_or_none()

    if user_already_exists:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "User already exists. Please login"
        )

    user = UserModel(
        name = data.name,
        email = data.email,
        password_hash = hash_password(password=data.password)
    )


    db.add(user)
    await db.commit()
    await db.refresh(user)


    return RegisterResponseSchema(
        user_id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at

    )




@auth_router.post("/login")
async def login_user(
    data : LoginRequestSchema,
    db : AsyncSession = Depends(get_db),
):
    email = data.email
    password = data.password

    user_check_query = (
        select(UserModel)
        .where(UserModel.email == email)
    )

    user_check_results = await db.execute(user_check_query)

    user = user_check_results.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid token"
        )

    password_verified = verify_password(hash_password=user.password_hash, password=password)

    if not password_verified:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid credenntials"
        )

    a_token = create_access_token(user_id=user.id)

    refresh_token_check_query = (
        select(RefreshTokenModel)
        .where(RefreshTokenModel.user_id == user.id)
    )

    refresh_token_check_result = await db.execute(refresh_token_check_query)

    refresh_token_exists = refresh_token_check_result.scalar_one_or_none()

    r_token = create_refresh_token()
    refresh_token_expiry = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRY_IN_DAYS)

    if not refresh_token_exists:
        refresh_token_object = RefreshTokenModel(
            user_id = user.id,
            refresh_token = r_token,
            refresh_token_expiry = refresh_token_expiry
        )

        db.add(refresh_token_object)

    else:
        refresh_token_object = refresh_token_exists
        refresh_token_object.refresh_token = r_token
        refresh_token_object.refresh_token_expiry = refresh_token_expiry
    await db.commit()
    await db.refresh(refresh_token_object)

    return LoginResponseSchema(
        user_id=user.id,
        name=user.name,
        email=user.email,
        access_token=a_token,
        access_token_expiry=settings.ACCESS_TOKEN_EXPIRY_IN_MINUTES * 60,
        refresh_token=refresh_token_object.refresh_token
    )


@auth_router.post("/refresh-token")
async def refresh_token(
    data : RefreshTokenRequestSchema,
    db : AsyncSession = Depends(get_db),
    user : UserModel = Depends(get_user)
):
    refresh_token_check_query = (
        select(RefreshTokenModel)
        .where(RefreshTokenModel.user_id == user.id)
        .where(RefreshTokenModel.refresh_token == data.refresh_token)
    )


    refresh_token_check_result = await db.execute(refresh_token_check_query)

    refresh_token_check = refresh_token_check_result.scalar_one_or_none()

    if refresh_token_check is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid token"
        )

    access_token = create_access_token(user_id=user.id)

    return RefreshTokenResponseSchema(
        access_token=access_token,
        access_token_expiry=settings.ACCESS_TOKEN_EXPIRY_IN_MINUTES * 60,
        refresh_token=refresh_token_check.refresh_token
    )
