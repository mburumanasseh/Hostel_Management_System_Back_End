from flask import Blueprint

from app.controllers.block_controller import (
    create_block,
    get_all_blocks,
    get_block,
    update_block,
    delete_block
)

from app.utils.authorization import role_required


block_bp = Blueprint(
    "blocks",
    __name__,
    url_prefix="/api/blocks"
)


# Admin and warden can create blocks
block_bp.route(
    "",
    methods=["POST"]
)(
    role_required("admin", "warden")(create_block)
)


# All authenticated users can view blocks
block_bp.route(
    "",
    methods=["GET"]
)(
    role_required(
        "admin",
        "warden",
        "student",
        "finance"
    )(get_all_blocks)
)


# All authenticated users can view a specific block
block_bp.route(
    "/<int:block_id>",
    methods=["GET"]
)(
    role_required(
        "admin",
        "warden",
        "student",
        "finance"
    )(get_block)
)


# Admin and warden can update blocks
block_bp.route(
    "/<int:block_id>",
    methods=["PUT"]
)(
    role_required("admin", "warden")(update_block)
)


# Only admin can delete blocks
block_bp.route(
    "/<int:block_id>",
    methods=["DELETE"]
)(
    role_required("admin")(delete_block)
)