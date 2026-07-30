from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
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
        required=False,
        validate=validate.OneOf([
            "student",
            "admin",
            "warden",
            "finance"
        ]),
        load_default="student"
    )


class LoginSchema(Schema):
    email = fields.Email(
        required=True
    )

    password = fields.Str(
        required=True,
        load_only=True
    )