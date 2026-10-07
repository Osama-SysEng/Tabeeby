"""Configuration for vr-ar-platform"""
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    service_name: str = "vr-ar-platform"
    port: int = 8025
    debug: bool = False
    database_url: str = "sqlite:///./vr-ar-platform.db"
    class Config: env_file = ".env"
