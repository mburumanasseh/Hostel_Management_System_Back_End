
from flask import Blueprint

from app.controllers.payment_controller import (
    create_payment,
    get_all_payments,
    get_payment,
    get_student_payments,
    get_my_payments,
    update_payment_status,
    delete_payment,
    get_my_financial_status,
    get_student_financial_status
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
    create_payment
)


# =====================================================
# GET ALL PAYMENTS
# ADMIN + FINANCE
# =====================================================

payment_bp.route(
    "",
    methods=["GET"]
)(
    get_all_payments
)


# =====================================================
# GET CURRENT STUDENT'S PAYMENTS
# STUDENT ONLY
# =====================================================

payment_bp.route(
    "/my",
    methods=["GET"]
)(
    get_my_payments
)


# =====================================================
# GET CURRENT STUDENT'S FINANCIAL STATUS
# STUDENT ONLY
# =====================================================

payment_bp.route(
    "/my/financial-status",
    methods=["GET"]
)(
    get_my_financial_status
)


# =====================================================
# GET ONE PAYMENT
# ADMIN + FINANCE
# =====================================================

payment_bp.route(
    "/<int:payment_id>",
    methods=["GET"]
)(
    get_payment
)


# =====================================================
# GET PAYMENTS FOR A SPECIFIC STUDENT
# ADMIN + FINANCE
# =====================================================

payment_bp.route(
    "/student/<int:student_id>",
    methods=["GET"]
)(
    get_student_payments
)


# =====================================================
# GET SPECIFIC STUDENT FINANCIAL STATUS
# ADMIN + FINANCE
# =====================================================

payment_bp.route(
    "/student/<int:student_id>/financial-status",
    methods=["GET"]
)(
    get_student_financial_status
)


# =====================================================
# UPDATE PAYMENT STATUS
# ADMIN + FINANCE
# =====================================================

payment_bp.route(
    "/<int:payment_id>/status",
    methods=["PATCH"]
)(
    update_payment_status
)


# =====================================================
# DELETE PAYMENT
# ADMIN ONLY
# =====================================================

payment_bp.route(
    "/<int:payment_id>",
    methods=["DELETE"]
)(
    delete_payment
)