from marshmallow import Schema, fields, validate


class AllocationSchema(Schema):

    student_id = fields.Int(
        required=True
    )

    room_id = fields.Int(
        required=True
    )


class AllocationUpdateSchema(Schema):

    status = fields.Str(
        required=True,
        validate=validate.OneOf([
            "Active",
            "Completed"
        ])
    )