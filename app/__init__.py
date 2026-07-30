"""
Application Factory

Creates and configures the Flask application.
"""

from flask import Flask
from flask_cors import CORS

from app.config import config
from app.extensions import db, migrate, jwt, bcrypt


def create_app(config_name="default"):
    """
    Creates the Flask application.
    """

    app = Flask(__name__)

    app.config.from_object(config[config_name])

    CORS(app)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Import models so Flask-Migrate detects them
    from app.models import (
        User,
        Student,
        Block,
        Room,
        Allocation,
        MaintenanceRequest,
        Payment,
    )

    # Register authentication routes
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return {
            "message": "Hostel Management API Running Successfully",
            "status": "success"
        }, 200

    return app