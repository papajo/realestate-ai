from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PROJECT_NAME: str = "AI Real Estate Investing API"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/realestate_ai"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_REFRESH_SECRET_KEY: str = "your-refresh-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AWS KMS
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    AWS_KMS_KEY_ID: str = ""
    
    # Hugging Face
    HUGGINGFACE_API_KEY: str = ""
    
    # Public Record APIs
    COUNTY_ASSESSOR_API_KEY: str = ""
    COUNTY_ASSESSOR_API_URL: str = "https://api.countyassessor.com"
    
    # CORS - can be set via CORS_ORIGINS env var (comma-separated)
    # Default includes localhost for development
    # For Vercel preview deployments, add all domains or use regex pattern
    _cors_origins_env = os.getenv("CORS_ORIGINS", "")
    _default_origins = ["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"]
    
    if _cors_origins_env:
        CORS_ORIGINS: List[str] = [origin.strip() for origin in _cors_origins_env.split(",")]
    else:
        CORS_ORIGINS: List[str] = _default_origins
    
    # Auto-add all Vercel preview domains if in development
    if settings.DEBUG:
        import re
        vercel_pattern = re.compile(r'https://realestate-.*\.vercel\.app')
        # This will be handled in main.py middleware
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

