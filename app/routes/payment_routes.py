from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.controllers.payment_controller import (
    create_payment,
    get_all_payments,
    get_payment,
    get_student_payments,
    get_my_payments,
    update_payment_status,
    delete_payment
)

from app.utils.authorization import role_required


payment_bp = Blueprint(
    "payments",
    __name__,
    url_prefix="/api/payments"
)


# =====================================================
# CREATE PAYMENT
# ADMIN + FINANCE
# =====================================================

payment_bp.route(
    "",
    methods=["POST"]
)(
    role_required(
        "admin",
        "finance"
    )(
        create_payment
    )
)


# =====================================================
# GET ALL PAYMENTS
# ADMIN + FINANCE + WARDEN
# =====================================================

payment_bp.route(
    "",
    methods=["GET"]
)(
    role_required(
        "admin",
        "finance",
        "warden"
    )(
        get_all_payments
    )
)


# =====================================================
# GET CURRENT STUDENT'S PAYMENTS
# STUDENT ONLY / AUTHENTICATED USERS
# =====================================================

payment_bp.route(
    "/my",
    methods=["GET"]
)(
    jwt_required()(
        get_my_payments
    )
)


# =====================================================
# GET ONE PAYMENT
# ADMIN + FINANCE + WARDEN
#
# Students use /my instead so they cannot request
# another student's payment by changing the ID.
# =====================================================

payment_bp.route(
    "/<int:payment_id>",
    methods=["GET"]
)(
    role_required(
        "admin",
        "finance",
        "warden"
    )(
        get_payment
    )
)


# =====================================================
# GET PAYMENTS FOR A SPECIFIC STUDENT
# ADMIN + FINANCE + WARDEN
#
# Students should use /my instead.
# =====================================================

payment_bp.route(
    "/student/<int:student_id>",
    methods=["GET"]
)(
    role_required(
        "admin",
        "finance",
        "warden"
    )(
        get_student_payments
    )
)


# =====================================================
# UPDATE PAYMENT STATUS
# ADMIN + FINANCE
# =====================================================

payment_bp.route(
    "/<int:payment_id>/status",
    methods=["PATCH"]
)(
    role_required(
        "admin",
        "finance"
    )(
        update_payment_status
    )
)


# =====================================================
# DELETE PAYMENT
# ADMIN ONLY
# =====================================================

payment_bp.route(
    "/<int:payment_id>",
    methods=["DELETE"]
)(
    role_required(
        "admin"
    )(
        delete_payment
    )
)