from dataclasses import dataclass, field
from typing import Sequence, Type

from marshmallow import Schema, fields


@dataclass
class Api:
    status_code: str = field()
    status_message: str = field()
    data: dict = field()

    class __Schema(Schema):
        status_code = fields.Str(required=True)
        status_message = fields.Str(required=True)
        data = fields.Raw(required=True)

    @classmethod
    def validate(
        cls, data_schema: Type[Schema], data: Sequence[dict] | dict, *, many: bool
    ) -> dict:
        schema = cls.__Schema()
        schema.data = fields.Nested(data_schema, required=True)
        if many:
            return schema.validate(data, many=many)
        else:
            return schema.validate(data)
