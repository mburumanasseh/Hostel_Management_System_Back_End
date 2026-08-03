
from flask import request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity
from app.models.student import Student

from app.schemas.maintenance_schema import (
    MaintenanceRequestSchema,
    MaintenanceStatusSchema
)

from app.services.maintenance_service import (
    MaintenanceService
)


maintenance_schema = MaintenanceRequestSchema()
maintenance_status_schema = MaintenanceStatusSchema()


def create_maintenance_request():

    try:
        data = maintenance_schema.load(
            request.get_json()
        )

        maintenance_request = (
            MaintenanceService.create_request(
                student_id=data["student_id"],
                room_id=data["room_id"],
                title=data["title"],
                description=data["description"],
                priority=data.get(
                    "priority",
                    "Medium"
                )
            )
        )

        return jsonify({
            "message": "Maintenance request created successfully",
            "request": maintenance_request.to_dict()
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


def get_all_maintenance_requests():

    try:

        requests = (
            MaintenanceService.get_all_requests()
        )

        return jsonify({
            "requests": [
                maintenance_request.to_dict()
                for maintenance_request in requests
            ]
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def get_maintenance_request(request_id):

    try:

        maintenance_request = (
            MaintenanceService.get_request_by_id(
                request_id
            )
        )

        if not maintenance_request:

            return jsonify({
                "error": "Maintenance request not found"
            }), 404

        return jsonify({
            "request": maintenance_request.to_dict()
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def get_student_maintenance_requests(
    student_id
):

    try:

        requests = (
            MaintenanceService.get_student_requests(
                student_id
            )
        )

        return jsonify({
            "requests": [
                maintenance_request.to_dict()
                for maintenance_request in requests
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


def update_maintenance_status(
    request_id
):

    try:

        data = maintenance_status_schema.load(
            request.get_json()
        )

        maintenance_request = (
            MaintenanceService.update_status(
                request_id=request_id,
                status=data["status"]
            )
        )

        return jsonify({
            "message": "Maintenance status updated successfully",
            "request": maintenance_request.to_dict()
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


def delete_maintenance_request(
    request_id
):

    try:

        MaintenanceService.delete_request(
            request_id
        )

        return jsonify({
            "message": "Maintenance request deleted successfully"
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def get_my_maintenance_requests():

    try:

        user_id = int(get_jwt_identity())

        student = Student.query.filter_by(
            user_id=user_id
        ).first()

        if not student:
            return jsonify({
                "error": "Student profile not found"
            }), 404

        requests = MaintenanceService.get_student_requests(
            student.id
        )

        return jsonify({
            "requests": [
                maintenance_request.to_dict()
                for maintenance_request in requests
            ]
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500