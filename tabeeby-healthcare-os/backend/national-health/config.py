"""Configuration for national-health"""
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    service_name: str = "national-health"
    port: int = 8010
    debug: bool = False
    database_url: str = "sqlite:///./national-health.db"
    class Config: env_file = ".env"
