from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=30,
                      description="Name cannot be blank and must have a max length of 30 characters")
    email: EmailStr = Field(..., max_length=30,
                            description="Email must be a valid email address with a max length of 30 characters")


class UserCreate(UserBase):
    password: str = Field(..., min_length=1, max_length=20,
                          description="Password cannot be blank and must have a max length of 20 characters")


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    pass
