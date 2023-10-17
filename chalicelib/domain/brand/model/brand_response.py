import re

from marshmallow import (
    EXCLUDE,
    Schema,
    fields,
)


class _BrandDetailMetaResponseSchema(Schema):
    description = fields.Str(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE


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

    class Meta:
        ordered = True
        unknown = EXCLUDE


class _BrandDetailProductResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    image = fields.URL(required=True, allow_none=True)
    image_alt = fields.Str(required=True)
    price = fields.Float(required=True)
    good_count: int = fields.Integer(required=True)

    class Meta:
        unknown = EXCLUDE


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

    class Meta:
        ordered = True
        unknown = EXCLUDE
