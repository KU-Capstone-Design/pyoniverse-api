from dataclasses import dataclass, field
from typing import List

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class SearchResultRequestDto(DtoIfs):
    query: str = field(default_factory=list)
    sort: str = field(default=None)
    direction: str = field(default=None)
    category: str = field(default=None)
    event: str = field(default=None)
    brand: str = field(default=None)
