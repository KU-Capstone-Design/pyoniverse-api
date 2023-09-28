from marshmallow import (
    EXCLUDE,
    INCLUDE,
    Schema,
    ValidationError,
    fields,
    validates_schema,
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

    class Meta:
        ordered = True
        unknown = EXCLUDE


class _BrandDetailProductItemResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    image = fields.URL(required=True, allow_none=True)
    image_alt = fields.Str(required=True)


class _BrandDetailProductResponseSchema(Schema):
    events = fields.List(fields.Str(), required=True)

    @validates_schema
    def validate_items(self, data, **kwargs):
        item_schema = _BrandDetailProductItemResponseSchema()
        events = data["events"]
        for event in events:
            if event not in data or len(data[event]) == 0:
                raise ValidationError(f"Event {event} not found in data", event)
            categories = data[event].keys()
            for category in categories:
                errors = item_schema.validate(data[event][category], many=True)
                if errors:
                    raise ValidationError("\n".join(errors), f"{event}.{category}")

    class Meta:
        order = True
        unknown = INCLUDE


class BrandDetailResponseSchema(Schema):
    slug = fields.Str(required=True)
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    meta = fields.Nested(_BrandDetailMetaResponseSchema, required=True)
    description = fields.Str(required=True)
    events = fields.Nested(_BrandDetailEventResponseSchema, many=True, required=True)
    products = fields.Nested(_BrandDetailProductResponseSchema, required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
