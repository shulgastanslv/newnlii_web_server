from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./chat.db"
    
    class Config:
        env_file = ".env"

settings = Settings()

