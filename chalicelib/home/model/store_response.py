from marshmallow import EXCLUDE, Schema, fields


class _HomeStoreResponseSchema(Schema):
    image = fields.URL(required=True)
    image_alt = fields.Str(required=True)
    name = fields.Str(required=True)
    brand = fields.Str(required=True)
    slug = fields.Str(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class HomeStoreResponseSchema(Schema):
    stores = fields.Nested(_HomeStoreResponseSchema, required=True, many=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
