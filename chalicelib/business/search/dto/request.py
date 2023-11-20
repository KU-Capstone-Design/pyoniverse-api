from dataclasses import dataclass, field

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class SearchResultRequestDto(DtoIfs):
    query: str = field(default_factory=list)
