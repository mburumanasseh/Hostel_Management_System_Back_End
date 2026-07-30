
from marshmallow import Schema, fields, validate


class MaintenanceRequestSchema(Schema):

    title = fields.Str(
        required=True,
        validate=validate.Length(
            min=3,
            max=150
        )
    )

    description = fields.Str(
        required=True,
        validate=validate.Length(
            min=5,
            max=1000
        )
    )

    priority = fields.Str(
        required=False,
        load_default="Medium",
        validate=validate.OneOf([
            "Low",
            "Medium",
            "High",
            "Urgent"
        ])
    )

    student_id = fields.Int(
        required=True
    )

    room_id = fields.Int(
        required=True
    )


class MaintenanceStatusSchema(Schema):

    status = fields.Str(
        required=True,
        validate=validate.OneOf([
            "Pending",
            "In Progress",
            "Resolved"
        ])
    )