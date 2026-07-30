
from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.controllers.maintenance_controller import (
    create_maintenance_request,
    get_all_maintenance_requests,
    get_maintenance_request,
    get_student_maintenance_requests,
    update_maintenance_status,
    delete_maintenance_request
)

from app.utils.authorization import role_required


maintenance_bp = Blueprint(
    "maintenance",
    __name__,
    url_prefix="/api/maintenance"
)


# ==========================================
# CREATE MAINTENANCE REQUEST
# ==========================================

maintenance_bp.route(
    "",
    methods=["POST"]
)(
    jwt_required()(
        create_maintenance_request
    )
)


# ==========================================
# GET ALL MAINTENANCE REQUESTS
# ADMIN + WARDEN ONLY
# ==========================================

maintenance_bp.route(
    "",
    methods=["GET"]
)(
    role_required(
        "admin",
        "warden"
    )(
        get_all_maintenance_requests
    )
)


# ==========================================
# GET ONE MAINTENANCE REQUEST
# ==========================================

maintenance_bp.route(
    "/<int:request_id>",
    methods=["GET"]
)(
    jwt_required()(
        get_maintenance_request
    )
)


# ==========================================
# GET STUDENT MAINTENANCE REQUESTS
# ==========================================

maintenance_bp.route(
    "/student/<int:student_id>",
    methods=["GET"]
)(
    jwt_required()(
        get_student_maintenance_requests
    )
)


# ==========================================
# UPDATE MAINTENANCE STATUS
# ADMIN + WARDEN ONLY
# ==========================================

maintenance_bp.route(
    "/<int:request_id>/status",
    methods=["PATCH"]
)(
    role_required(
        "admin",
        "warden"
    )(
        update_maintenance_status
    )
)


# ==========================================
# DELETE MAINTENANCE REQUEST
# ADMIN ONLY
# ==========================================

maintenance_bp.route(
    "/<int:request_id>",
    methods=["DELETE"]
)(
    role_required(
        "admin"
    )(
        delete_maintenance_request
    )
)
