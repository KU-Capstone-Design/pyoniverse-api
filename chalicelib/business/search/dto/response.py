from dataclasses import dataclass, field
from typing import List

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class SearchHomeResponseDto(DtoIfs):
    histories: List[str] = field(default_factory=list)
