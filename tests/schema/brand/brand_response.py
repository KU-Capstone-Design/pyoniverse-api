import re

from marshmallow import (
    Schema,
    fields,
)


class _BrandDetailMetaResponseSchema(Schema):
    description = fields.Str(required=True)


class _BrandDetailEventResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    brand = fields.Str(required=True)
    image = fields.URL(required=True, allow_none=True)
    image_alt = fields.Str(required=True)
    start_at = fields.Str(
        required=True, validate=lambda x: re.match(r"\d{4}-\d{2}-\d{2}", x)
    )
    end_at = fields.Str(
        required=True, validate=lambda x: re.match(r"\d{4}-\d{2}-\d{2}", x)
    )
    good_count: int = fields.Integer(required=True)
    view_count: int = fields.Integer(required=True)


class _BrandDetailProductResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    image = fields.URL(required=True, allow_none=True)
    image_alt = fields.Str(required=True)
    price = fields.Float(required=True)
    event_price = fields.Float(required=True, allow_none=True)
    events = fields.List(fields.Str(), required=True)
    good_count: int = fields.Integer(required=True)
    view_count: int = fields.Integer(required=True)


class BrandDetailResponseSchema(Schema):
    slug = fields.Str(required=True)
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    meta = fields.Nested(_BrandDetailMetaResponseSchema, required=True)
    description = fields.Str(required=True)
    events = fields.Nested(_BrandDetailEventResponseSchema, many=True, required=True)
    products = fields.Nested(
        _BrandDetailProductResponseSchema, required=True, many=True
    )
    image = fields.URL(required=True)
    image_alt = fields.Str(required=True)
