"""Configuration for ai-physician"""
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    service_name: str = "ai-physician"
    port: int = 8021
    debug: bool = False
    database_url: str = "sqlite:///./ai-physician.db"
    class Config: env_file = ".env"
