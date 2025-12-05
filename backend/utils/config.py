"""
Configuration Management for HoneyGo Backend

Uses Pydantic Settings for environment variable management and validation.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Settings
    app_name: str = "HoneyGo Dynamic Pricing API"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"
    
    # Server Configuration
    backend_port: int = 8000
    backend_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:3000"
    
    # MongoDB Configuration
    mongodb_uri: str = "mongodb://localhost:27017/honeygo"
    
    # ChromaDB Configuration
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    chroma_persist_directory: str = "./chromadb_data"
    
    # LLM Provider (OpenAI)
    openai_api_key: Optional[str] = None
    
    # LangSmith Observability
    langchain_api_key: Optional[str] = None
    langchain_tracing_v2: bool = True
    langchain_project: str = "HoneyGo-Hackathon"
    
    # External APIs (Optional)
    weather_api_key: Optional[str] = None
    events_api_key: Optional[str] = None
    traffic_api_key: Optional[str] = None
    
    # Logging
    log_level: str = "info"
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create a global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Dependency function to get settings instance
    
    Returns:
        Settings: The application settings
    """
    return settings

