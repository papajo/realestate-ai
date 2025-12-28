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
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"]
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

