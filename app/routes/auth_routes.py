
from flask import Blueprint

from app.controllers.auth_controller import (
    register,
    register_staff,
    login,
    get_current_user
)


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


# ==========================================
# STUDENT REGISTRATION
# ==========================================

auth_bp.route(
    "/register",
    methods=["POST"]
)(
    register
)


# ==========================================
# STAFF REGISTRATION
# ADMIN ONLY
# ==========================================

auth_bp.route(
    "/staff",
    methods=["POST"]
)(
    register_staff
)


# ==========================================
# LOGIN
# ==========================================

auth_bp.route(
    "/login",
    methods=["POST"]
)(
    login
)


# ==========================================
# CURRENT USER
# ==========================================

auth_bp.route(
    "/me",
    methods=["GET"]
)(
    get_current_user
)