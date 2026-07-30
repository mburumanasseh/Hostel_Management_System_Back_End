from flask import request, jsonify
from marshmallow import ValidationError

from app.schemas.room_schema import (
    RoomSchema,
    RoomUpdateSchema
)

from app.services.room_service import RoomService


room_schema = RoomSchema()
room_update_schema = RoomUpdateSchema()


def create_room():

    try:
        data = room_schema.load(
            request.get_json()
        )

        room = RoomService.create_room(
            block_id=data["block_id"],
            room_number=data["room_number"],
            floor=data["floor"],
            capacity=data["capacity"],
            occupied=data.get("occupied", 0),
            status=data.get("status", "Available")
        )

        return jsonify({
            "message": "Room created successfully",
            "room": room.to_dict()
        }), 201

    except ValidationError as error:

        return jsonify({
            "error": error.messages
        }), 400

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 409

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def get_all_rooms():

    try:
        rooms = RoomService.get_all_rooms()

        return jsonify({
            "rooms": [
                room.to_dict()
                for room in rooms
            ]
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def get_room(room_id):

    try:
        room = RoomService.get_room_by_id(
            room_id
        )

        if not room:
            return jsonify({
                "error": "Room not found"
            }), 404

        return jsonify({
            "room": room.to_dict()
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def get_rooms_by_block(block_id):

    try:
        rooms = RoomService.get_rooms_by_block(
            block_id
        )

        return jsonify({
            "rooms": [
                room.to_dict()
                for room in rooms
            ]
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def update_room(room_id):

    try:
        data = room_update_schema.load(
            request.get_json()
        )

        room = RoomService.update_room(
            room_id,
            data
        )

        return jsonify({
            "message": "Room updated successfully",
            "room": room.to_dict()
        }), 200

    except ValidationError as error:

        return jsonify({
            "error": error.messages
        }), 400

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def delete_room(room_id):

    try:
        RoomService.delete_room(
            room_id
        )

        return jsonify({
            "message": "Room deleted successfully"
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500