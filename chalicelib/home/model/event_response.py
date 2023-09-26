from marshmallow import EXCLUDE, Schema, fields


class _HomeEventResponseSchema(Schema):
    image = fields.URL(required=True)
    image_alt = fields.Str(required=True)
    name = fields.Str(required=True)
    id = fields.Int(required=True)
    brand = fields.Str(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class HomeEventResponseSchema(Schema):
    events = fields.Nested(_HomeEventResponseSchema, required=True, many=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
