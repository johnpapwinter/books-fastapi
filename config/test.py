from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    DATABASE_URL: str = "sqlite:///test.db"
    JWT_SECRET: str = "test_secret_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    ADMIN_USERNAME: str = "test_admin"
    ADMIN_EMAIL: str = "test@example.com"
    ADMIN_PASSWORD: str = "test_password"
    ENV: str = "test"

