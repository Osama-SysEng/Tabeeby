"""Configuration for edge-computing"""
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    service_name: str = "edge-computing"
    port: int = 8026
    debug: bool = False
    database_url: str = "sqlite:///./edge-computing.db"
    class Config: env_file = ".env"
