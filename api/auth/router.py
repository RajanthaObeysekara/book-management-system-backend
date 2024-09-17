from fastapi import APIRouter, status, Depends, Header
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from api.constants import route_paths
from api.db.database import get_db
from api.auth.service import get_token, get_refresh_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(route_paths.route_auth_token, status_code=status.HTTP_200_OK)
async def authenticate_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await get_token(data=data, db=db)


@router.post(route_paths.route_auth_refresh, status_code=status.HTTP_200_OK)
async def refresh_access_token(refresh_token: str = Header(), db: Session = Depends(get_db)):
    return await get_refresh_token(token=refresh_token, db=db)
