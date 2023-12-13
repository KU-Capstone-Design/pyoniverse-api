from dataclasses import dataclass, field
from typing import Sequence, Type

from marshmallow import EXCLUDE, Schema, fields


@dataclass
class Api:
    status_code: str = field()
    status_message: str = field()
    data: dict = field()

    class __Schema(Schema):
        status_code = fields.Str(required=True)
        status_message = fields.Str(required=True)

        class Meta:
            unknown = EXCLUDE

    @classmethod
    def validate(
        cls, data_schema: Type[Schema], data: Sequence[dict] | dict, *, many: bool
    ) -> dict:
        schema = cls.__Schema()
        # schema.data = fields.Nested(data_schema, required=True)
        res = {}
        if many:
            res["api_validation"] = schema.validate(data, many=many)
        else:
            res["api_validation"] = schema.validate(data)
        if isinstance(data, list):
            nested_data = [body["data"] for body in data]
            res["nested_data"] = data_schema().validate(nested_data, many=True)
        else:
            nested_data = data["data"]
            res["nested_data"] = data_schema().validate(nested_data)
        if res["api_validation"] == {} and res["nested_data"] == {}:
            return {}
        else:
            return res
