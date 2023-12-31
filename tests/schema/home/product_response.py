from marshmallow import Schema, fields


class _HomeProductResponseSchema(Schema):
    image = fields.URL(required=True)
    image_alt = fields.Str(required=True)
    name = fields.Str(required=True)
    id = fields.Int(required=True)
    events = fields.List(fields.Integer(), required=True)
    price = fields.Float(required=True)
    event_price = fields.Float(required=True, allow_none=True)
    event_brand = fields.Str(required=True)
    good_count: int = fields.Integer(required=True)


class HomeProductResponseSchema(Schema):
    products = fields.Nested(_HomeProductResponseSchema, required=True, many=True)
