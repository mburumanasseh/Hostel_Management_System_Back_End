from functools import wraps

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt


def role_required(*allowed_roles):

    def decorator(function):

        @wraps(function)
        @jwt_required()
        def wrapper(*args, **kwargs):

            claims = get_jwt()
            user_role = claims.get("role")

            if user_role not in allowed_roles:
                return jsonify({
                    "error": "Access denied",
                    "message": "You do not have permission to access this resource"
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator

from app.utils.authorization import role_required

@role_required("admin")
def admin_test():

    return jsonify({
        "message": "Welcome Admin!",
        "status": "success"
    }), 200