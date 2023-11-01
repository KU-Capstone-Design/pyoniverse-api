from marshmallow import Schema, fields


class ProductBrandHistoryResponseSchema(Schema):
    date = fields.Date(required=True, format="iso")
    events = fields.List(fields.Str(), required=True)
    price = fields.Float(required=True)
    event_price = fields.Float(required=True, allow_none=True)


class ProductBrandResponseSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.Str(required=True)
    image = fields.URL(required=True)
    events = fields.List(fields.Str(), required=True)
    event_price = fields.Float(required=True, allow_none=True)
    price = fields.Float(required=True)
    histories = fields.Nested(
        ProductBrandHistoryResponseSchema, required=True, many=True
    )


class ProductResponseSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    image = fields.URL(required=True)
    image_alt = fields.Str(required=True)
    best_brand = fields.Integer(required=True)
    brands = fields.Nested(ProductBrandResponseSchema, required=True, many=True)
    good_count = fields.Integer(required=True)
    view_count = fields.Integer(required=True)
