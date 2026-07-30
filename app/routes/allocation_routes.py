from flask import Blueprint

from app.controllers.allocation_controller import (
    create_allocation,
    get_all_allocations,
    get_allocation,
    get_student_allocations,
    get_active_allocation,
    complete_allocation,
    delete_allocation
)

from app.utils.authorization import role_required


allocation_bp = Blueprint(
    "allocations",
    __name__,
    url_prefix="/api/allocations"
)


# Admin and warden can allocate rooms
allocation_bp.route(
    "",
    methods=["POST"]
)(
    role_required("admin", "warden")(create_allocation)
)


# Admin and warden can view all allocations
allocation_bp.route(
    "",
    methods=["GET"]
)(
    role_required("admin", "warden")(get_all_allocations)
)


# Admin and warden can view a specific allocation
allocation_bp.route(
    "/<int:allocation_id>",
    methods=["GET"]
)(
    role_required("admin", "warden")(get_allocation)
)


# Admin and warden can view a student's allocation history
allocation_bp.route(
    "/student/<int:student_id>",
    methods=["GET"]
)(
    role_required("admin", "warden")(get_student_allocations)
)


# Admin, warden and student can view active allocation
allocation_bp.route(
    "/student/<int:student_id>/active",
    methods=["GET"]
)(
    role_required(
        "admin",
        "warden",
        "student"
    )(get_active_allocation)
)


# Admin and warden can complete allocations
allocation_bp.route(
    "/<int:allocation_id>/complete",
    methods=["PUT"]
)(
    role_required("admin", "warden")(complete_allocation)
)


# Only admin can delete allocations
allocation_bp.route(
    "/<int:allocation_id>",
    methods=["DELETE"]
)(
    role_required("admin")(delete_allocation)
)