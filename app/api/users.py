from datetime import datetime, timedelta
from typing import Annotated

from api.deps import PasswordRequestDep, SessionDep, get_current_user
from config import settings
from db import crud, schemas
from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from utils.hashing import verify_password

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

router = APIRouter(tags=["users"])


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Возвращение токена доступа JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def verify_token(token: str) -> str | None:
    """Декодирование JWT токена."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        return None


def authenticated_user(db: SessionDep, email, password):
    user = crud.get_user_by_email(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/token/")
def login_access_token(db: SessionDep, form_data: PasswordRequestDep):
    user = authenticated_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный email или пароль.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/", response_model=list[schemas.User])
def user_list(db: SessionDep):
    """Список пользователей."""
    users = crud.get_users(db)
    return users


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: SessionDep):
    """Создание пользователя."""
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return crud.create_user(db=db, user=user)


@router.get("/users/me/")
def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    return current_user
