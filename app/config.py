from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SYNC_DATABASE_URL: str
    SECRET_KEY: str
    ADMIN_API_KEY: str
    ENVIRONMENT: str = "development"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    RESEND_API_KEY: str
    NOTIFY_EMAIL: str
    FROM_EMAIL: str
    FRONTEND_URL: str = "http://localhost:3000"
      # 7 days
    class Config:
        env_file = ".env"

settings = Settings()