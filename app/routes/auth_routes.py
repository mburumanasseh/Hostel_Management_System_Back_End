from flask import Blueprint

from app.controllers.auth_controller import (
    register,
    login,
    get_current_user
)

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)

auth_bp.route(
    "/register",
    methods=["POST"]
)(register)

auth_bp.route(
    "/login",
    methods=["POST"]
)(login)

auth_bp.route(
    "/me",
    methods=["GET"]
)(get_current_user)

