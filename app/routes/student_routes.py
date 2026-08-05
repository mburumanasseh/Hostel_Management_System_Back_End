from flask import Blueprint

from app.controllers.student_controller import (
    create_student,
    get_students,
    get_student,
    update_student,
    delete_student
)


student_bp = Blueprint(
    "students",
    __name__,
    url_prefix="/api/students"
)


# ============================================================
# CREATE
# ============================================================

student_bp.route(
    "",
    methods=["POST"]
)(create_student)


# ============================================================
# GET ALL
# ============================================================

student_bp.route(
    "",
    methods=["GET"]
)(get_students)


# ============================================================
# GET ONE
# ============================================================

student_bp.route(
    "/<int:student_id>",
    methods=["GET"]
)(get_student)


# ============================================================
# UPDATE
# ============================================================

student_bp.route(
    "/<int:student_id>",
    methods=["PUT"]
)(update_student)


# ============================================================
# DELETE
# ============================================================

student_bp.route(
    "/<int:student_id>",
    methods=["DELETE"]
)(delete_student)