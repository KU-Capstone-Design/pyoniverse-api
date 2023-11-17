from marshmallow import Schema, fields


class SearchHomeResponseSchema(Schema):
    recommendations = fields.List(fields.Str(), required=True)
    histories = fields.List(fields.Str(), required=True)
