from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.schemas.student_schema import StudentSchema
from app.services.student_service import StudentService
from app.utils.authorization import role_required


student_schema = StudentSchema()


@role_required("admin", "warden")
def create_student():

    try:
        data = student_schema.load(
            request.get_json()
        )

        student = StudentService.create_student(
            user_id=data["user_id"],
            registration_number=data["registration_number"],
            gender=data.get("gender"),
            phone=data.get("phone"),
            course=data.get("course"),
            year_of_study=data.get("year_of_study"),
            guardian_name=data.get("guardian_name"),
            guardian_phone=data.get("guardian_phone")
        )

        return jsonify({
            "message": "Student created successfully",
            "student": student.to_dict()
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


@jwt_required()
def get_students():

    try:
        students = StudentService.get_all_students()

        return jsonify({
            "students": [
                student.to_dict()
                for student in students
            ]
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


@jwt_required()
def get_student(student_id):

    try:
        student = StudentService.get_student_by_id(
            student_id
        )

        if not student:
            return jsonify({
                "error": "Student not found"
            }), 404

        return jsonify({
            "student": student.to_dict()
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


@role_required("admin", "warden")
def update_student(student_id):

    try:
        data = student_schema.load(
            request.get_json(),
            partial=True
        )

        student = StudentService.update_student(
            student_id,
            data
        )

        return jsonify({
            "message": "Student updated successfully",
            "student": student.to_dict()
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


@role_required("admin")
def delete_student(student_id):

    try:
        StudentService.delete_student(
            student_id
        )

        return jsonify({
            "message": "Student deleted successfully"
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500