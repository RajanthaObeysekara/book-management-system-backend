from fastapi.exceptions import HTTPException
from fastapi import status
from datetime import timedelta, datetime
from jose import jwt
from api.auth.schema import TokenResponse
from api.constants import messages
from api.user.model import User
from api.auth.security import get_token_payload
from api.core.config import get_settings
from api.auth.security import verify_password

settings = get_settings()


async def get_token(data, db):
    user = db.query(User).filter(User.email == data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=messages.USER_NOT_FOUND,
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=messages.INVALID_LOGIN_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await _get_user_token(user=user)


async def get_refresh_token(token, db):
    payload = get_token_payload(token=token)
    user_id = payload.get('id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.INVALID_REFRESH_TOKEN,
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.INVALID_REFRESH_TOKEN,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await _get_user_token(user=user, refresh_token=token)


async def _get_user_token(user: User, refresh_token=None):
    payload = {"id": user.id}

    access_token_expiry = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = await create_access_token(payload, access_token_expiry)
    if not refresh_token:
        refresh_token = await create_refresh_token(payload)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds
    )


async def create_access_token(data,  expiry: timedelta):
    payload = data.copy()
    expire_in = datetime.now() + expiry
    payload.update({"exp": expire_in})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


async def create_refresh_token(data):
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
