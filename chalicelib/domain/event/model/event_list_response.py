from marshmallow import Schema, fields


class EventListItemSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.Str(required=True)
    start_at = fields.Date(required=True, format="iso")
    end_at = fields.Date(required=True, format="iso")
    image = fields.URL(required=True)
    image_alt = fields.Str(required=True)
    view_count = fields.Integer(required=True)
    good_count = fields.Integer(required=True)


class EventListResponseSchema(Schema):
    brand_list = fields.List(fields.Str(), required=True)
    brnad_slug = fields.Str(required=True)
    brand_name = fields.Str(required=True)
    brand_image = fields.URL(required=True)
    events = fields.Nested(EventListItemSchema, required=True, many=True)
