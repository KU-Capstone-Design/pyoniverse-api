from marshmallow import Schema, fields


class ProductBrandHistoryResponseSchema(Schema):
    date = fields.Date(required=True, format="%Y-%m")
    events = fields.List(fields.Str(), required=True)
    price = fields.Float(required=True)
    event_price = fields.Float(required=True, allow_none=True)


class ProductBrandHistoriesSummaryPriceSchema(Schema):
    brand = fields.Str(required=True)
    date = fields.Date(required=True, format="%Y-%m")
    value = fields.Float(required=True)


class ProductBrandHistoriesSummarySchema(Schema):
    # 행사 가격 기준으로 최저, 최고가 명시
    lowest_price = fields.Nested(ProductBrandHistoriesSummaryPriceSchema, required=True)
    highest_price = fields.Nested(
        ProductBrandHistoriesSummaryPriceSchema, required=True
    )


class ProductBrandResponseSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.Str(required=True)
    image = fields.URL(required=True)
    events = fields.List(fields.Str(), required=True)
    event_price = fields.Float(required=True, allow_none=True)
    price = fields.Float(required=True)
    histories = fields.Nested(
        ProductBrandHistoryResponseSchema, required=True, many=True
    )
    histories_summary = fields.Nested(ProductBrandHistoriesSummarySchema, required=True)


class ProductResponseSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    image = fields.URL(required=True)
    image_alt = fields.Str(required=True)
    best_brand = fields.Integer(required=True)
    brands = fields.Nested(ProductBrandResponseSchema, required=True, many=True)
    good_count = fields.Integer(required=True)
    view_count = fields.Integer(required=True)
