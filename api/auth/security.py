from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from fastapi import Depends
from api.user.model import User
from api.db.database import get_db
from api.core.config import get_settings

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_token_payload(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET,
                             algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None
    return payload


def get_current_user(token: str = Depends(oauth2_scheme), db=None):
    payload = get_token_payload(token)
    if not payload or type(payload) is not dict:
        return None

    user_id = payload.get('id', None)
    if not user_id:
        return None

    if not db:
        db = next(get_db())

    user = db.query(User).filter(User.id == user_id).first()
    return user


class JWTAuth:

    async def authenticate(self, conn):
        guest = AuthCredentials(['unauthenticated']), UnauthenticatedUser()

        if 'authorization' not in conn.headers:
            return guest

        token = conn.headers.get('authorization').split(' ')[1]
        if not token:
            return guest

        user = get_current_user(token=token)

        if not user:
            return guest

        return AuthCredentials('authenticated'), user
