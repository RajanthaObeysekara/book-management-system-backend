from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from api.user.service import create_user
from api.db.database import get_db
from api.user.schema import UserCreate, UserResponse
from api.auth.security import oauth2_scheme
from api.constants import route_paths, responses

# unauthenticated route
router = APIRouter(
    prefix=route_paths.route_prefix_user,
    tags=route_paths.route_prefix_users_tags,
    responses=responses.get_not_found_response(),
)

# authenticated route
user_router = APIRouter(
    prefix=route_paths.route_prefix_user,
    tags=route_paths.route_prefix_users_tags,
    responses=responses.get_not_found_response(),
    dependencies=[Depends(oauth2_scheme)]
)


@router.post(route_paths.route_user_create, status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@user_router.post(route_paths.route_user_me, status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_detail(request: Request):
    return request.user
