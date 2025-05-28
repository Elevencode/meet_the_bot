"""
Configuration module for the backend service.
Handles environment variables and application settings.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8001
    debug: bool = False
    
    # Google API configuration
    google_service_account_path: str = "service-account.json"
    google_impersonation_email: Optional[str] = None  # Email to impersonate for Meet creation
    
    # Telegram Bot configuration
    telegram_bot_token: Optional[str] = None
    
    # Logging configuration
    log_level: str = "INFO"
    
    model_config = {
        "env_file": "/Users/arthur/dev/meet_the_bot/.env",  # Absolute path to .env in project root
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "env_prefix": "",
        # Environment variable mappings
        "env_nested_delimiter": "__",
    }


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings 