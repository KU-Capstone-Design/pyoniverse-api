from dataclasses import dataclass, field
from typing import Literal, Sequence

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class SearchEngineResponseDto(DtoIfs):
    version: str = field(default=None)
    engine_type: Literal["ML", "ALGORITHM"] = field(default=None)
    results: Sequence[int] = field(default_factory=list)
