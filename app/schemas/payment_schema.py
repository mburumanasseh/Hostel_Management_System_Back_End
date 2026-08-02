from marshmallow import Schema, fields, validate


class PaymentSchema(Schema):

    student_id = fields.Int(
        required=True
    )

    amount = fields.Decimal(
        required=True,
        as_string=False,
        validate=validate.Range(
            min=0.01
        )
    )

    semester = fields.Str(
        required=True,
        validate=validate.Length(
            min=2,
            max=30
        )
    )

    status = fields.Str(
        required=False,
        load_default="Pending",
        validate=validate.OneOf([
            "Pending",
            "Paid",
            "Failed"
        ])
    )

    reference_number = fields.Str(
        required=True,
        validate=validate.Length(
            min=3,
            max=100
        )
    )


class PaymentStatusSchema(Schema):

    status = fields.Str(
        required=True,
        validate=validate.OneOf([
            "Pending",
            "Paid",
            "Failed"
        ])
    )