from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Configurações da aplicação"""

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/financeiro"

    # JWT & Security
    SECRET_KEY: str = "sua-chave-secreta-super-segura-min-32-caracteres"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    REFRESH_TOKEN_EXPIRATION_DAYS: int = 7

    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: str = "csv,pdf,xlsx"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    # Email
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_EMAIL: str = "seu-email@gmail.com"
    SMTP_PASSWORD: str = "sua-senha-app"

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def cors_origins_list(self) -> List[str]:
        """Converte string de origins para lista"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def allowed_types_list(self) -> List[str]:
        """Converte string de tipos permitidos para lista"""
        return [ftype.strip() for ftype in self.ALLOWED_FILE_TYPES.split(",")]

    @property
    def max_upload_bytes(self) -> int:
        """Converte MB para bytes"""
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024


# Instância global
settings = Settings()
