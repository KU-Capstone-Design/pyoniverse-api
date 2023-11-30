import typing
from dataclasses import dataclass, field

from chalice import BadRequestError
from marshmallow import RAISE, Schema, fields, types, validate

from chalicelib.business.interface.dto import DtoIfs


class _SearchResultRequestDtoSchema(Schema):
    query = fields.Str(required=True)
    page = fields.Int(required=False, load_default=1)
    page_size = fields.Int(required=False, load_default=10)
    sort_key = fields.Str(
        required=False,
        validate=validate.OneOf(["price", "event_price", "good_count", "view_count"]),
        load_default="event_price",
    )
    sort_direction = fields.Str(
        required=False, validate=validate.OneOf(["asc", "desc"]), load_default="asc"
    )

    class Meta:
        unknown = RAISE

    def load(
        self,
        data: (
            typing.Mapping[str, typing.Any]
            | typing.Iterable[typing.Mapping[str, typing.Any]]
        ),
        *,
        many: bool | None = None,
        partial: bool | types.StrSequenceOrSet | None = None,
        unknown: str | None = None,
    ) -> "SearchResultRequestDto":
        res = super().load(data)
        return SearchResultRequestDto(**res)


@dataclass(kw_only=True)
class SearchResultRequestDto(DtoIfs):
    query: str = field(default_factory=list)
    page: int = field(default=1)
    page_size: int = field(default=10)
    sort_key: str = field(default="event_price")
    sort_direction: str = field(default="asc")

    @classmethod
    def validate(cls, request: typing.Mapping):
        errors = _SearchResultRequestDtoSchema().validate(request)
        if errors:
            raise BadRequestError(f"잘못된 요청입니다\n{errors}")

    @classmethod
    def load(cls, request: typing.Mapping) -> "SearchResultRequestDto":
        cls.validate(request)
        return _SearchResultRequestDtoSchema().load(request, unknown=RAISE)
