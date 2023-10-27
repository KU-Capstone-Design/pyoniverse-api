from dataclasses import dataclass, field

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class HomeRequestDto(DtoIfs):
    type: str = field(default=None)
