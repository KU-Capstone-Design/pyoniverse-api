from marshmallow import Schema, fields


class SearchHomeResponseSchema(Schema):
    histories = fields.List(fields.Str(), required=True)
