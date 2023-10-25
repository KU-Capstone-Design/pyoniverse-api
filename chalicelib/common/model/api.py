from dataclasses import dataclass, field
from typing import Type

from marshmallow import EXCLUDE, Schema, fields


@dataclass
class Api:
    status_code: str = field()
    status_message: str = field()
    data: dict = field()
    # errors: Optional[List[str]] = field(default=None)
    # pagination: Optional[Pagination] = field(default=None)


class ApiSchema:
    @staticmethod
    def get_schema(data_schema: Type[Schema]) -> Schema:
        class Nested(Schema):
            status_code = fields.Str(required=True)
            status_message = fields.Str(required=True)
            data = fields.Nested(data_schema, required=True)

            class Meta:
                unknown = EXCLUDE
                ordered = True

        return Nested()
