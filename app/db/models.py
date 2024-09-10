from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    birthday = Column(Date)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    posts = relationship("Post", back_populates="author")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})"

    def __str__(self):
        return f"Пользователь {self.email}"


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    pub_date = Column(DateTime, server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})"

    def __str__(self):
        return f"Пост: {self.title}"
