from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    # Базовый URL для webhook callbacks
    
    class Config:
        env_file = ".env"

settings = Settings()
