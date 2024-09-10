from db import crud, database, schemas
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=list[schemas.Post])
def post_list(db: Session = Depends(get_db)):  # noqa: B008
    posts = crud.get_posts(db)
    return posts


@app.get("/users/", response_model=list[schemas.User])
def user_list(db: Session = Depends(get_db)):  # noqa: B008
    users = crud.get_users(db)
    return users


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):  # noqa: B008
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
