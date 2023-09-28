from marshmallow import EXCLUDE, Schema, fields


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

    class Meta:
        ordered = True
        unknown = EXCLUDE


class _BrandDetailProductItemResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    image = fields.URL(required=True, allow_none=True)
    image_alt = fields.Str(required=True)


class _BrandDetailProductResponseSchema(Schema):
    event = fields.Str(required=True)
    category = fields.Str(required=True)
    items = fields.Nested(
        _BrandDetailProductItemResponseSchema, many=True, required=True
    )


class BrandDetailResponseSchema(Schema):
    slug = fields.Str(required=True)
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    meta = fields.Nested(_BrandDetailMetaResponseSchema, required=True)
    description = fields.Str(required=True)
    events = fields.Nested(_BrandDetailEventResponseSchema, many=True, required=True)
    products = fields.Nested(
        _BrandDetailProductResponseSchema, many=True, required=True
    )

    class Meta:
        ordered = True
        unknown = EXCLUDE
