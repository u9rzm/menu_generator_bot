import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Bot settings"""
    
    # Bot settings
    BOT_TOKEN: str
    API_URL: str
    NGINX_URL: str
    IMAGES_URL: str
    BACKGROUNDS_URL: str
    GEN_URL: str
    
    # Database settings
    DATABASE_URL: Optional[str] = None
    
    # File settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: list[str] = ["image/jpeg", "image/png", "image/gif"]
    ALLOWED_MENU_TYPES: list[str] = ["text/csv"]
    
    # Theme settings
    DEFAULT_THEME: str = "default"
    THEME_PREVIEW_SIZE: tuple[int, int] = (800, 600)
    
    # QR code settings
    QR_CODE_SIZE: int = 10
    QR_CODE_VERSION: int = 1
    QR_CODE_ERROR_CORRECTION: int = 0
    
    # Web page settings
    WEB_PAGE_TITLE: str = "Меню организации"
    WEB_PAGE_DESCRIPTION: str = "Онлайн-меню вашей организации"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create settings instance
settings = Settings() 