from marshmallow import Schema, fields


class SearchResultCategoryResponseSchema(Schema):
    id = fields.Integer(required=True, allow_none=True)
    name = fields.Str(required=True)


class SearchResultEventResponseSchema(Schema):
    id = fields.Integer(required=True, allow_none=True)
    name = fields.Str(required=True)


class SearchResultBrandResponseSchema(Schema):
    id = fields.Integer(required=True, allow_none=True)
    name = fields.Str(required=True)
    image = fields.URL(required=True)


class SearchResultProductSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.Str(required=True)
    image = fields.URL(required=True)
    image_alt = fields.Str(required=True)
    price = fields.Float(required=True)
    events = fields.List(fields.Str(), required=True)
    event_price = fields.Float(required=True, allow_none=True)
    category = fields.Integer(required=True, allow_none=True)
    brands = fields.List(fields.Integer(), required=True, validate=lambda x: len(x) > 0)


class SearchResultResponseSchema(Schema):
    categories = fields.Nested(
        SearchResultCategoryResponseSchema, required=True, many=True
    )
    events = fields.Nested(SearchResultEventResponseSchema, required=True, many=True)
    brands = fields.Nested(SearchResultBrandResponseSchema, required=True, many=True)
    products = fields.Nested(SearchResultProductSchema, required=True, many=True)
