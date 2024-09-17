from email import message
import os
import uuid
import shutil
from typing import List
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Request, HTTPException, UploadFile, File
from fastapi import status
from api.book.model import Book
from api.user.model import User
from api.book.schema import BookResponse
from api.user.service import validate_user_non_availability_id
from api.constants import messages

# base url for the uploaded images
base_url = os.getenv('BASE_URL', 'http://localhost:8000/download/')


# create the file uploading directory if it doesn't exist
UPLOAD_DIRECTORY = "images"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


async def create_book(request,  db, title, author, isbn, book_image, publishd_date, category):
    # validate the user existance
    db_user = validate_user_non_availability_id(db=db, id=request.user.id)

    # remove blanks from the image name
    unique_filename = f"{uuid.uuid4()}_{book_image.filename.replace(' ', '_')}"
    image_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)

    # Save the uploaded image to a local file
    image_path = f"{UPLOAD_DIRECTORY}/{unique_filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(book_image.file, buffer)
    db_book = Book(title=title, author=author, ISBN=isbn, publication_date=publishd_date,
                   user_id=db_user.id, cover_image=unique_filename, category=category)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return [db_book]


def get_book_by_id(db: Session, id: int, request: Request):
    db_user = validate_user_non_availability_id(db=db, id=request.user.id)
    db_books = db.query(Book).filter(
        Book.id == id, Book.user_id == db_user.id).first()
    if db_books is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=messages)

    return update_book_cover_image_url(db_books)


def update_book_cover_image_url(db_books: List[Book]):
    updated_books = []
    for book in db_books:
        book_dict = book.__dict__.copy()  # Convert the SQLAlchemy model to a dict
        if not book.cover_image.startswith(base_url):
            book_dict["cover_image"] = f"{base_url}{book.cover_image}"
        updated_books.append(BookResponse.model_validate(
            book_dict))  # Validate with Pydantic
    return updated_books


def get_all_books(db: Session,  request: Request):
    db_user = validate_user_non_availability_id(db=db, id=request.user.id)
    db_books = db.query(Book).filter(Book.user_id == db_user.id).order_by(
        Book.created_time.desc()).all()
    return update_book_cover_image_url(db_books)


def delete_book_by_id(request: Request, db: Session, id: int):
    db_user = db.query(User).filter(User.id == request.user.id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=messages.USER_NOT_FOUND)
    book = db.query(Book).filter(
        Book.id == id, Book.user_id == db_user.id).first()
    if not book:
        return None
    db.delete(book)
    db.commit()
    return True


async def update_book(request: Request, db: Session, book_id: int, title: str, author: str, isbn: str, publishd_date: str, category: str, book_image: Optional[UploadFile]):
    db_user = validate_user_non_availability_id(db=db, id=request.user.id)

    db_book = db.query(Book).filter(Book.id == book_id,
                                    Book.user_id == db_user.id).first()
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=messages.BOOK_NOT_FOUND)

    # Update fields
    db_book.title = title
    db_book.author = author
    db_book.ISBN = isbn
    db_book.publication_date = publishd_date
    db_book.category = category

    # Update image if provided
    if book_image:
        unique_filename = f"{uuid.uuid4()}_{
            book_image.filename.replace(' ', '_')}"
        image_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(book_image.file, buffer)
        db_book.cover_image = unique_filename
    db.commit()
    db.refresh(db_book)

    return BookResponse.model_validate(db_book.__dict__)
