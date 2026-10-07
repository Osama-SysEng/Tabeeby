"""Configuration for drug-discovery"""
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    service_name: str = "drug-discovery"
    port: int = 8023
    debug: bool = False
    database_url: str = "sqlite:///./drug-discovery.db"
    class Config: env_file = ".env"
