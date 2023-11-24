import re

from marshmallow import Schema, fields


class _HomeEventResponseSchema(Schema):
    image = fields.URL(required=True)
    image_alt = fields.Str(required=True)
    name = fields.Str(required=True)
    id = fields.Int(required=True)
    brand = fields.Str(required=True)
    start_at = fields.Str(
        required=True, validate=lambda x: re.match(r"\d{4}-\d{2}-\d{2}", x)
    )
    end_at = fields.Str(
        required=True, validate=lambda x: re.match(r"\d{4}-\d{2}-\d{2}", x)
    )


class HomeEventResponseSchema(Schema):
    events = fields.Nested(_HomeEventResponseSchema, required=True, many=True)
