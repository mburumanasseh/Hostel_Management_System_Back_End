
from flask import request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity, get_jwt

from app.schemas.allocation_schema import AllocationSchema

from app.services.allocation_service import AllocationService
from app.services.student_service import StudentService


allocation_schema = AllocationSchema()


def create_allocation():

    try:
        data = allocation_schema.load(
            request.get_json()
        )

        allocation = AllocationService.create_allocation(
            student_id=data["student_id"],
            room_id=data["room_id"]
        )

        return jsonify({
            "message": "Room allocated successfully",
            "allocation": allocation.to_dict()
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


def get_all_allocations():

    try:
        allocations = (
            AllocationService.get_all_allocations()
        )

        return jsonify({
            "allocations": [
                allocation.to_dict()
                for allocation in allocations
            ]
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def get_allocation(allocation_id):

    try:
        allocation = (
            AllocationService.get_allocation_by_id(
                allocation_id
            )
        )

        if not allocation:
            return jsonify({
                "error": "Allocation not found"
            }), 404

        return jsonify({
            "allocation": allocation.to_dict()
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def get_student_allocations(student_id):

    try:
        allocations = (
            AllocationService.get_student_allocations(
                student_id
            )
        )

        return jsonify({
            "allocations": [
                allocation.to_dict()
                for allocation in allocations
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


def get_active_allocation(student_id):

    try:
        user_id = get_jwt_identity()
        claims = get_jwt()

        user_role = claims.get("role")

        # Students can only view their own allocation
        if user_role == "student":

            student = StudentService.get_student_by_user_id(
                int(user_id)
            )

            if not student:
                return jsonify({
                    "error": "Student profile not found"
                }), 404

            if student.id != student_id:
                return jsonify({
                    "error": "Access denied",
                    "message": "You can only view your own allocation"
                }), 403

        allocation = (
            AllocationService.get_active_allocation(
                student_id
            )
        )

        if not allocation:
            return jsonify({
                "message": "Student has no active allocation",
                "allocation": None
            }), 200

        return jsonify({
            "allocation": allocation.to_dict()
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def get_my_allocation():

    try:
        user_id = get_jwt_identity()

        student = StudentService.get_student_by_user_id(
            int(user_id)
        )

        if not student:
            return jsonify({
                "error": "Student profile not found"
            }), 404

        allocation = (
            AllocationService.get_active_allocation(
                student.id
            )
        )

        if not allocation:
            return jsonify({
                "message": "You have no active room allocation",
                "allocation": None
            }), 200

        return jsonify({
            "allocation": allocation.to_dict()
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def complete_allocation(allocation_id):

    try:
        allocation = (
            AllocationService.complete_allocation(
                allocation_id
            )
        )

        return jsonify({
            "message": "Allocation completed successfully",
            "allocation": allocation.to_dict()
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def delete_allocation(allocation_id):

    try:
        AllocationService.delete_allocation(
            allocation_id
        )

        return jsonify({
            "message": "Allocation deleted successfully"
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def book_room():
    """
    Logged-in student books a room for themselves.
    Body: { "room_id": <int> }
    """
    try:
        data = request.get_json() or {}
        room_id = data.get("room_id")

        if room_id is None:
            return jsonify({
                "error": "room_id is required"
            }), 400

        try:
            room_id = int(room_id)
        except (TypeError, ValueError):
            return jsonify({
                "error": "room_id must be an integer"
            }), 400

        user_id = int(get_jwt_identity())

        allocation = AllocationService.book_room(
            user_id=user_id,
            room_id=room_id
        )

        return jsonify({
            "message": "Room booked successfully",
            "allocation": allocation.to_dict()
        }), 201

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 409

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


def get_available_rooms_for_booking():
    """
    List rooms that still have free beds.
    Students use this when choosing a room.
    """
    try:
        rooms = AllocationService.get_available_rooms()
        return jsonify({
            "count": len(rooms),
            "rooms": [room.to_dict() for room in rooms]
        }), 200
    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500
