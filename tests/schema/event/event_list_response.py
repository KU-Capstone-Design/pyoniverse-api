from marshmallow import Schema, fields


class EventListItemSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.Str(required=True)
    start_at = fields.Date(required=True, format="%m/%d")
    end_at = fields.Date(required=True, format="%m/%d")
    image = fields.URL(required=True)
    image_alt = fields.Str(required=True)
    view_count = fields.Integer(required=True)
    good_count = fields.Integer(required=True)


class EventListBrandSchema(Schema):
    slug = fields.Str(required=True)
    name = fields.Str(required=True)
    image = fields.URL(required=True)


class EventListResponseSchema(Schema):
    brands = fields.Nested(EventListBrandSchema, required=True, many=True)
    brand_slug = fields.Str(required=True)
    brand_name = fields.Str(required=True)
    events = fields.Nested(EventListItemSchema, required=True, many=True)
