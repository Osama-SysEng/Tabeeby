"""Configuration for virtual-nanobot"""
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    service_name: str = "virtual-nanobot"
    port: int = 8024
    debug: bool = False
    database_url: str = "sqlite:///./virtual-nanobot.db"
    class Config: env_file = ".env"
