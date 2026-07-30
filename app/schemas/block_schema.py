from marshmallow import Schema, fields, validate


class BlockSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=20)
    )

    gender = fields.Str(
        required=True,
        validate=validate.OneOf([
            "Male",
            "Female",
            "Mixed"
        ])
    )


class BlockUpdateSchema(Schema):
    name = fields.Str(
        required=False,
        validate=validate.Length(min=1, max=20)
    )

    gender = fields.Str(
        required=False,
        validate=validate.OneOf([
            "Male",
            "Female",
            "Mixed"
        ])
    )