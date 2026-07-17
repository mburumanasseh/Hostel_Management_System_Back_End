"""
Application configuration settings.

This file loads environment variables from the .env file
and makes them available to the Flask application.
"""

import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()


class Config:
    """Base configuration class."""

    SECRET_KEY = os.getenv("SECRET_KEY")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://"
        f"{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False