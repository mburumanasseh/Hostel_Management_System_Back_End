from marshmallow import Schema, fields, validate


class StudentSchema(Schema):

    user_id = fields.Int(required=True)

    registration_number = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=30)
    )

    gender = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.OneOf([
            "Male",
            "Female"
        ])
    )

    phone = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=20)
    )

    course = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=100)
    )

    year_of_study = fields.Int(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1, max=10)
    )

    guardian_name = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=100)
    )

    guardian_phone = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=20)
    )