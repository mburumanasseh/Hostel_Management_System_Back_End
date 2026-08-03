from functools import wraps

from flask import jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity
)


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
                    "message": (
                        "You do not have permission "
                        "to access this resource"
                    )
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator


def get_current_user_id():
    """
    Return the ID of the currently authenticated user.
    """

    return int(get_jwt_identity())