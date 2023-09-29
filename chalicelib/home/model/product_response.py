from marshmallow import EXCLUDE, Schema, fields


class _HomeProductResponseSchema(Schema):
    image = fields.URL(required=True)
    image_alt = fields.Str(required=True)
    name = fields.Str(required=True)
    id = fields.Int(required=True)
    events = fields.Str(validate=lambda x: x is None, required=True, allow_none=True)
    price = fields.Float(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class HomeProductResponseSchema(Schema):
    products = fields.Nested(_HomeProductResponseSchema, required=True, many=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
