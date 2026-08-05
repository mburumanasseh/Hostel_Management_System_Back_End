
from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    """
    Public registration schema.

    This endpoint is for student accounts only.
    """

    first_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    last_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    email = fields.Email(
        required=True
    )

    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=6)
    )

    registration_number = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=30)
    )


class StaffRegisterSchema(Schema):
    """
    Staff account creation schema.

    Only administrators should be able to use
    the endpoint that uses this schema.
    """

    first_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    last_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    email = fields.Email(
        required=True
    )

    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=6)
    )

    role = fields.Str(
        required=True,
        validate=validate.OneOf([
            "admin",
            "warden",
            "finance"
        ])
    )


class LoginSchema(Schema):

    email = fields.Email(
        required=True
    )

    password = fields.Str(
        required=True,
        load_only=True
    )