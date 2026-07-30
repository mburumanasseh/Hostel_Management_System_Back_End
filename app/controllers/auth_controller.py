from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from marshmallow import ValidationError

from app.schemas.auth_schema import (
    RegisterSchema,
    LoginSchema
)

from app.services.auth_service import AuthService


register_schema = RegisterSchema()
login_schema = LoginSchema()


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
            role=data.get("role", "student")
        )

        return jsonify({
            "message": "User registered successfully",
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
        
@jwt_required()
def get_current_user():

    try:
        user_id = get_jwt_identity()

        user = AuthService.get_user_by_id(user_id)

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
        
        
