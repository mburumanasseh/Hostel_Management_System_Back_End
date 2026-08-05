from flask import Blueprint

from app.controllers.hostel_fee_controller import (
    create_hostel_fee,
    get_all_hostel_fees,
    get_hostel_fee,
    update_hostel_fee,
    delete_hostel_fee
)

from app.utils.authorization import role_required


hostel_fee_bp = Blueprint(
    "hostel_fees",
    __name__,
    url_prefix="/api/hostel-fees"
)


# =====================================================
# CREATE HOSTEL FEE
# ADMIN ONLY
# =====================================================

hostel_fee_bp.route(
    "",
    methods=["POST"]
)(
    role_required("admin")(
        create_hostel_fee
    )
)


# =====================================================
# GET ALL HOSTEL FEES
# ADMIN + FINANCE
# =====================================================

hostel_fee_bp.route(
    "",
    methods=["GET"]
)(
    role_required(
        "admin",
        "finance"
    )(
        get_all_hostel_fees
    )
)


# =====================================================
# GET ONE HOSTEL FEE
# ADMIN + FINANCE
# =====================================================

hostel_fee_bp.route(
    "/<int:fee_id>",
    methods=["GET"]
)(
    role_required(
        "admin",
        "finance"
    )(
        get_hostel_fee
    )
)


# =====================================================
# UPDATE HOSTEL FEE
# ADMIN ONLY
# =====================================================

hostel_fee_bp.route(
    "/<int:fee_id>",
    methods=["PUT"]
)(
    role_required("admin")(
        update_hostel_fee
    )
)


# =====================================================
# DELETE HOSTEL FEE
# ADMIN ONLY
# =====================================================

hostel_fee_bp.route(
    "/<int:fee_id>",
    methods=["DELETE"]
)(
    role_required("admin")(
        delete_hostel_fee
    )
)