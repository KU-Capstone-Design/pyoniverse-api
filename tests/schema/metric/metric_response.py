from marshmallow import Schema, fields


class MetricResponseSchema(Schema):
    id = fields.Integer(required=True)
    domain = fields.Str(required=True)
    value = fields.Integer(required=True)
