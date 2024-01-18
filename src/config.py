from typing import ClassVar
from pydantic_settings import (
    BaseSettings,
)
import os

class Setting(BaseSettings):
    DATABASE_URL: ClassVar[str] = os.environ.get('DATABASE_URL')
    GOOGLE_MAP_API_KEY: ClassVar[str] = os.environ.get('GOOGLE_MAP_API_KEY')
    REDIS_HOST: ClassVar[str] = os.environ.get('REDIS_HOST')
    REDIS_PORT: ClassVar[int] = os.environ.get('REDIS_PORT')
    REDIS_PASSWORD: ClassVar[str] = os.environ.get('REDIS_PASSWORD')
    FRONTEND_URL: ClassVar[str] = os.environ.get('FRONTEND_URL')

setting = Setting()
