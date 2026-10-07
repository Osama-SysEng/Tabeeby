"""Configuration for ultra-iq-integration"""
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    service_name: str = "ultra-iq-integration"
    port: int = 8009
    debug: bool = False
    database_url: str = "sqlite:///./ultra-iq-integration.db"
    class Config: env_file = ".env"
