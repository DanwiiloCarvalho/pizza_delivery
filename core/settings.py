from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    DATABASE_URL: str
    API_PREFIX: str
    ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str
    REFRESH_TOKEN_EXPIRE_DAYS: str
    POSTGRES_USER: str | None
    POSTGRES_DB: str | None
    POSTGRES_PASSWORD: str | None

    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    model_config = SettingsConfigDict(case_sensitive=True, env_file='.env')

    class DBBaseModel(DeclarativeBase):
        pass


settings = Settings()
