from fastapi import APIRouter, Depends, Request, Form, File, UploadFile, status, HTTPException
from sqlalchemy.orm import Session
from api.book.service import create_book, get_book_by_id, get_all_books, delete_book_by_id, update_book
from api.db.database import get_db
from api.book.schema import BookResponse, BooksCreate
from api.auth.security import oauth2_scheme
from api.constants import responses, route_paths, messages


router = APIRouter(
    prefix=route_paths.route_prefix_book,
    tags=route_paths.route_prefix_books_tags,
    dependencies=[Depends(oauth2_scheme)],
    responses=responses.get_not_found_response(),
)


@router.get(route_paths.route_book_get_id, response_model=BookResponse)
def get_book(request: Request, item_id: int, db: Session = Depends(get_db)):
    return get_book_by_id(db=db, id=item_id,  request=request)


@router.get(route_paths.route_book_get_all)
def get_all_user_books(request: Request, db: Session = Depends(get_db)):
    return get_all_books(db=db, request=request)


@router.post(route_paths.route_book_post, response_model=list[BookResponse])
async def create_new_book(request: Request, title=Form(...), author=Form(...), isbn=Form(...), publishDate=Form(...), category=Form(...), bookImage: UploadFile = File(), db: Session = Depends(get_db)):
    return await create_book(request=request, db=db, title=title, author=author, isbn=isbn, book_image=bookImage, publishd_date=publishDate, category=category)


@router.put(route_paths.route_book_update, response_model=BookResponse)
async def update_existing_book(
    request: Request,
    item_id: int,
    title=Form(...), author=Form(...), isbn=Form(...),
    publishDate=Form(...), category=Form(...),
    bookImage: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    return await update_book(
        request=request, db=db, book_id=item_id,
        title=title, author=author, isbn=isbn,
        book_image=bookImage, publishd_date=publishDate,
        category=category
    )


@router.delete(route_paths.route_book_delete)
async def delete_book(request: Request, item_id: int, db: Session = Depends(get_db)):
    deleted = delete_book_by_id(request=request, db=db, id=item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.BOOK_NOT_FOUND)
    return {"detail": messages.BOOK_DELETED_SUCCESSFUL}
