from flask import Blueprint

from app.controllers.payment_controller import (
    create_payment,
    get_all_payments,
    get_payment,
    get_student_payments,
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
# GET ONE PAYMENT
# =====================================================

payment_bp.route(
    "/<int:payment_id>",
    methods=["GET"]
)(
    role_required(
        "admin",
        "finance",
        "warden",
        "student"
    )(
        get_payment
    )
)


# =====================================================
# GET STUDENT PAYMENTS
# =====================================================

payment_bp.route(
    "/student/<int:student_id>",
    methods=["GET"]
)(
    role_required(
        "admin",
        "finance",
        "warden",
        "student"
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
