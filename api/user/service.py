from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api.user.model import User
from api.user.schema import UserCreate
from api.auth.security import get_password_hash
from api.constants import messages


def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()


def validate_user_availability(db: Session, email: str):
    user = get_user(db, email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=messages.USER_ALREADY_EXISTS)
    return user


def validate_user_non_availability_id(db: Session, id: str):
    user = get_user_by_id(db, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=messages.USER_NOT_FOUND)
    return user


def create_user(db: Session, data: UserCreate):
    validate_user_availability(db, email=data.email)
    db_user = User(name=data.name, email=data.email,
                   password=get_password_hash(data.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return JSONResponse(
        content={"message": messages.USER_CREATED_SUCCESSFUL},
        status_code=status.HTTP_201_CREATED
    )
