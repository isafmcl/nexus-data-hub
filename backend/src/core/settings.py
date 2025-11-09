from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = Field(default="Nexus Data Hub", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    

    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"], 
        env="CORS_ORIGINS"
    )
    
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    redis_db: int = Field(default=0, env="REDIS_DB")
    

    rate_limit_enabled: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=3600, env="RATE_LIMIT_WINDOW")  # 1 hora
    

    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")  # json ou text
    

    cache_ttl: int = Field(default=3600, env="CACHE_TTL")  # 1 hora
    cache_enabled: bool = Field(default=True, env="CACHE_ENABLED")
    
    openweather_api_key: Optional[str] = Field(default=None, env="OPENWEATHER_API_KEY")
    newsapi_key: Optional[str] = Field(default=None, env="NEWSAPI_KEY")
    awesome_api_key: Optional[str] = Field(default=None, env="AWESOME_API_KEY")
    app_secret: Optional[str] = Field(default=None, env="APP_SECRET")
    
    api_endpoints: dict = {
        "weather": "https://api.openweathermap.org/data/2.5",
        "news": "https://newsapi.org/v2",
        "openlibrary": "https://openlibrary.org",
        "worldbank": "https://api.worldbank.org/v2",
        "countries": "https://restcountries.com/v3.1",
        "viacep": "https://viacep.com.br/ws"
    }
    
    http_timeout: int = Field(default=30, env="HTTP_TIMEOUT")
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
