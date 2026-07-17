"""
Application factory.

Creates and configures the Flask application.
"""

from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import db, migrate, jwt, bcrypt


def create_app():
    """Application factory."""

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Enable CORS for React frontend
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    @app.route("/")
    def home():
        return {
            "message": "Hostel Management API is running!",
            "status": "success"
        }

    return app