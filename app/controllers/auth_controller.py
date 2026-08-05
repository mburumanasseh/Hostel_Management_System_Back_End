from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from marshmallow import ValidationError

from app.schemas.auth_schema import (
    RegisterSchema,
    StaffRegisterSchema,
    LoginSchema
)

from app.services.auth_service import AuthService
from app.utils.authorization import role_required


register_schema = RegisterSchema()
staff_register_schema = StaffRegisterSchema()
login_schema = LoginSchema()


# ==========================================
# STUDENT REGISTRATION
# ==========================================

def register():

    try:

        data = register_schema.load(
            request.get_json()
        )

        user = AuthService.register_user(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
            registration_number=data["registration_number"]
        )

        return jsonify({
            "message": "Student account registered successfully",
            "user": user.to_dict()
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


# ==========================================
# STAFF REGISTRATION
# ==========================================

@role_required("admin")
def register_staff():

    try:

        data = staff_register_schema.load(
            request.get_json()
        )

        user = AuthService.register_staff(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
            role=data["role"]
        )

        return jsonify({
            "message": "Staff account created successfully",
            "user": user.to_dict()
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


# ==========================================
# LOGIN
# ==========================================

def login():

    try:

        data = login_schema.load(
            request.get_json()
        )

        user, access_token = AuthService.login_user(
            email=data["email"],
            password=data["password"]
        )

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": user.to_dict()
        }), 200

    except ValidationError as error:

        return jsonify({
            "error": error.messages
        }), 400

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 401

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ==========================================
# CURRENT USER
# ==========================================

@jwt_required()
def get_current_user():

    try:

        user_id = get_jwt_identity()

        user = AuthService.get_user_by_id(
            user_id
        )

        if not user:

            return jsonify({
                "error": "User not found"
            }), 404

        return jsonify({
            "user": user.to_dict()
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500