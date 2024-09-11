import os

from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    app_name: str = "Yatube"
    SECRET_KEY: str = "keep-it-secret-keep-it-safe"
    ALGORITHM: str = "HS256"
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    DATABASE_URL: str = f"sqlite:///{os.path.join(BASE_DIR, 'dbase.db')}"


settings = Setting()
