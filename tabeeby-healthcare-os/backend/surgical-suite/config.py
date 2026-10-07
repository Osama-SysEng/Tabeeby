"""Configuration for surgical-suite"""
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    service_name: str = "surgical-suite"
    port: int = 8008
    debug: bool = False
    database_url: str = "sqlite:///./surgical-suite.db"
    class Config: env_file = ".env"
