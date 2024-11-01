from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = 'books-fastapi'
    DEBUG: bool = False
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_HOURS: int
    ADMIN_USERNAME: str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    class Config:
        env_file = '.env'

