from marshmallow import Schema, fields


class EventDetailResponseSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.Str(required=True)
    brand_slug = fields.Str(required=True)
    brand_name = fields.Str(required=True)
    view_count = fields.Integer(required=True)
    good_count = fields.Integer(required=True)
    images = fields.List(fields.URL(required=True), required=True)
    image_alt = fields.Str(required=True)
    start_at = fields.Date(required=True, format="iso")
    end_at = fields.Date(required=True, format="iso")
    link = fields.URL(required=True)
