from marshmallow import Schema, fields, validate


class RoomSchema(Schema):
    block_id = fields.Int(
        required=True
    )

    room_number = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=20)
    )

    floor = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    capacity = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    occupied = fields.Int(
        required=False,
        validate=validate.Range(min=0),
        load_default=0
    )

    status = fields.Str(
        required=False,
        validate=validate.OneOf([
            "Available",
            "Occupied",
            "Maintenance"
        ]),
        load_default="Available"
    )


class RoomUpdateSchema(Schema):
    block_id = fields.Int(
        required=False
    )

    room_number = fields.Str(
        required=False,
        validate=validate.Length(min=1, max=20)
    )

    floor = fields.Int(
        required=False,
        validate=validate.Range(min=0)
    )

    capacity = fields.Int(
        required=False,
        validate=validate.Range(min=1)
    )

    occupied = fields.Int(
        required=False,
        validate=validate.Range(min=0)
    )

    status = fields.Str(
        required=False,
        validate=validate.OneOf([
            "Available",
            "Occupied",
            "Maintenance"
        ])
    )