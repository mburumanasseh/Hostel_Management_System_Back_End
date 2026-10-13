"""
Application configuration.

This module loads environment variables and provides
configuration classes for different environments.
"""

import os
from datetime import timedelta

from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


def _database_uri():
    """
    Prefer DATABASE_URL (Render / Heroku style).
    Fall back to individual DB_* variables for local setup.
    """
    url = os.getenv("DATABASE_URL")
    if url:
        # Render sometimes provides postgres:// — SQLAlchemy needs postgresql://
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        # Ensure psycopg2 driver is explicit when scheme is bare postgresql
        if url.startswith("postgresql://") and "+psycopg2" not in url:
            url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return url

    return (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )


class Config:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)

    SQLALCHEMY_DATABASE_URI = _database_uri()

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
