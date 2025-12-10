import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    """Application Settings and conifguration"""

    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = int(os.getenv("DATABAE_PORT", 5432))
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "authdb")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "authuser")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "authpassword")

    @property
    def DATABASE_URL(self)-> str:
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "auth-system-prod-secret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    
    CSRF_SECRET_KEY: str = os.getenv("CSRF_SECRET_KEY", "auth-csrf-secret")

    ENVOIRONMENT: str = os.getenv("ENVOIRONMENT", "development")

    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", 8000))


    #cors
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

settings = Settings()