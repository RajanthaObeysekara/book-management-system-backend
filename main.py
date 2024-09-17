import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi import HTTPException


# route imports
from api.user.router import router as guest_router
from api.user.router import user_router
from api.auth.router import router as auth_router
from api.book.router import router as book_router

# model imports
from api.book import model as book_model
from api.user import model as user_model

# database imports
from api.db.database import engine

# middlewares
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from api.auth.security import JWTAuth

book_model.Base.metadata.create_all(bind=engine)
user_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# adding routers
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(book_router)
app.include_router(auth_router)


# bind origins as a middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())


UPLOAD_DIRECTORY = "images"
# fetch all the images from this endpoint


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

# backend checking route


@app.get("/info")
def read_root():
    return {"Levin Test Assignment written by Rajantha"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
