from api.deps import SessionDep
from db import crud, schemas
from fastapi import APIRouter

router = APIRouter(tags=["posts"])


@router.get("/posts", response_model=list[schemas.Post])
def post_list(db: SessionDep):
    posts = crud.get_posts(db)
    return posts
