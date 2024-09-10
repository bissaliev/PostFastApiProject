from datetime import date, datetime

from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    description: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    pub_date: datetime
    author_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    birthday: date


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool = True
    is_superuser: bool = False
    posts: list[Post] = []

    class Config:
        orm_mode = True
