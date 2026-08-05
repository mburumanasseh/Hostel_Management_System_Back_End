from marshmallow import Schema, fields, validate


class HostelFeeSchema(Schema):

    semester = fields.Str(
        required=True,
        validate=validate.Length(
            min=2,
            max=30
        )
    )

    amount = fields.Decimal(
        required=True,
        as_string=False,
        validate=validate.Range(
            min=0.01
        )
    )