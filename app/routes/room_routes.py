from flask import Blueprint

from app.controllers.room_controller import (
    create_room,
    get_all_rooms,
    get_room,
    get_rooms_by_block,
    update_room,
    delete_room
)

from app.utils.authorization import role_required


room_bp = Blueprint(
    "rooms",
    __name__,
    url_prefix="/api/rooms"
)


# Admin and warden can create rooms
room_bp.route(
    "",
    methods=["POST"]
)(
    role_required("admin", "warden")(create_room)
)


# All authenticated users can view rooms
room_bp.route(
    "",
    methods=["GET"]
)(
    role_required(
        "admin",
        "warden",
        "student",
        "finance"
    )(get_all_rooms)
)


# All authenticated users can view a specific room
room_bp.route(
    "/<int:room_id>",
    methods=["GET"]
)(
    role_required(
        "admin",
        "warden",
        "student",
        "finance"
    )(get_room)
)


# All authenticated users can view rooms in a block
room_bp.route(
    "/block/<int:block_id>",
    methods=["GET"]
)(
    role_required(
        "admin",
        "warden",
        "student",
        "finance"
    )(get_rooms_by_block)
)


# Admin and warden can update rooms
room_bp.route(
    "/<int:room_id>",
    methods=["PUT"]
)(
    role_required("admin", "warden")(update_room)
)


# Only admin can delete rooms
room_bp.route(
    "/<int:room_id>",
    methods=["DELETE"]
)(
    role_required("admin")(delete_room)
)