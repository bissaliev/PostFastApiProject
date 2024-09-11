from api import posts, users
from fastapi import FastAPI

app = FastAPI(title="Yatube")

app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
def index():
    return {"message": "Hello User"}
