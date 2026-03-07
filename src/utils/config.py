# """Configuration management module."""

# import os
# from functools import lru_cache
# from typing import List, Optional

# from dotenv import load_dotenv
# from pydantic_settings import BaseSettings

# # Load environment variables from .env file
# load_dotenv()


# class Settings(BaseSettings):
#     """Application settings loaded from environment variables."""
    
#     # ============================================
#     # LLM Configuration
#     # ============================================
#     OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
#     OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
#     OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
    
#     GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
#     GOOGLE_MODEL: str = os.getenv("GOOGLE_MODEL", "gemini-pro")
    
#     DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", "gpt")
    
#     # ============================================
#     # Database Configuration
#     # ============================================
#     DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/business_data.db")
#     DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "False") == "True"
#     DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "5"))
#     DATABASE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))
    
#     # ============================================
#     # API Configuration
#     # ============================================
#     API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
#     API_PORT: int = int(os.getenv("API_PORT", "8000"))
#     API_DEBUG: bool = os.getenv("API_DEBUG", "False") == "True"
#     API_RELOAD: bool = os.getenv("API_RELOAD", "True") == "True"
    
#     CORS_ORIGINS: List[str] = [
#         "http://localhost:3000",
#         "http://localhost:8501",
#         "http://localhost:8000"
#     ]
#     CORS_CREDENTIALS: bool = True
#     CORS_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE"]
#     CORS_HEADERS: List[str] = ["*"]
    
#     # ============================================
#     # Application Configuration
#     # ============================================
#     ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
#     APP_NAME: str = os.getenv("APP_NAME", "AI Assistant for Business Data")
#     APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
#     LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
#     # ============================================
#     # Query Configuration
#     # ============================================
#     QUERY_TIMEOUT: int = int(os.getenv("QUERY_TIMEOUT", "30"))
#     MAX_RESPONSE_ROWS: int = int(os.getenv("MAX_RESPONSE_ROWS", "1000"))
#     MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1000"))
    
#     # ============================================
#     # Security Configuration
#     # ============================================
#     SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
#     JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key-here")
#     JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
#     JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    
#     # ============================================
#     # Rate Limiting
#     # ============================================
#     RATE_LIMIT_QUERIES_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_QUERIES_PER_MINUTE", "60"))
#     RATE_LIMIT_DATA_UPLOADS_PER_HOUR: int = int(os.getenv("RATE_LIMIT_DATA_UPLOADS_PER_HOUR", "20"))
    
#     # ============================================
#     # Data Processing
#     # ============================================
#     MAX_UPLOAD_FILE_SIZE: int = int(os.getenv("MAX_UPLOAD_FILE_SIZE", "50"))
#     ALLOWED_FILE_FORMATS: str = os.getenv("ALLOWED_FILE_FORMATS", "csv,xlsx,xls")
    
#     # ============================================
#     # Feature Flags
#     # ============================================
#     ENABLE_QUERY_HISTORY: bool = os.getenv("ENABLE_QUERY_HISTORY", "True") == "True"
#     ENABLE_QUERY_CACHING: bool = os.getenv("ENABLE_QUERY_CACHING", "True") == "True"
#     ENABLE_DATA_VALIDATION: bool = os.getenv("ENABLE_DATA_VALIDATION", "True") == "True"
#     ENABLE_API_METRICS: bool = os.getenv("ENABLE_API_METRICS", "True") == "True"
    
#     # ============================================
#     # Caching
#     # ============================================
#     CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "True") == "True"
#     CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "300"))
    
#     class Config:
#         env_file = ".env"
#         case_sensitive = True


# @lru_cache()
# def get_settings() -> Settings:
#     """
#     Get cached settings instance.
#     Uses caching to avoid reloading environment variables multiple times.
#     """
#     return Settings()
