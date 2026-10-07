"""Configuration for diagnostic-ai"""
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    service_name: str = "diagnostic-ai"
    port: int = 8022
    debug: bool = False
    database_url: str = "sqlite:///./diagnostic-ai.db"
    class Config: env_file = ".env"
